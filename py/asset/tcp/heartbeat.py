import threading
import logging as logging2

HEARTBEAT_OK = "OK"


class HeartBeat(threading.Thread):
    def __init__(self, client):
        self._client = client
        self._ids = []
        self._stop = threading.Event()
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def register(self, id_param):
        assert id_param not in self._ids
        self._ids.append(id_param)

    def unregister(self, id_param):
        assert id_param in self._ids
        self._ids.remove(id_param)

    def stop(self):
        self._stop.set()

    def run(self):
        try:
            while not self._stop.wait(5):
                if len(self._ids) == 0:
                    continue
                response = self._client.call('heartbeat', ids=self._ids)
                if response != HEARTBEAT_OK:
                    logging2.error("Asset heartbeat failed: '%(message)s'", dict(message=response))
                    raise Exception("Asset heartbeat failed: '%s'" % response)
        except:
            logging2.exception("Asset heartbeat thread dies")
            raise
        finally:
            if not self._stop.isSet():
                logging2.error("heartbeat thread notifies client about failure")
                self._client.heartbeatFailed()
            else:
                logging2.info("closing heartbeat thread in an orderly fashion")
