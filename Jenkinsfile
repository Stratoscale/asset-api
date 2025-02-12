@Library('library')_
String workSpace = "./workspace/${JOB_NAME}/$BUILD_NUMBER"
pipeline {
    agent {
        node {
            customWorkspace workSpace
            label 'jenkinsSlave'
        }
    }
    options {
        ansiColor('xterm')
        timestamps()
    }
    parameters {
        // Monkey branch for MonkeyTesting
        string(
            name: 'MONKEY_BRANCH',
            defaultValue: 'stable',
            description: 'Use Monkey at specific branch. For example: release_v22.02.0')
        // Monkey tests filter for MonkeyTesting
        string(
            name: 'MONKEY_TESTING_FILTER',
            defaultValue: '--regex chimp',
            description: 'Tests filter for MonkeyTesting')
        // Monkey additional params for MonkeyTesting
        string(
            name: 'ADDITIONAL_MONKEY_PARAMS',
            defaultValue: '',
            description: 'Monkey additional parameters')
    }
    environment {
        // Get HEAD commit massage
        GIT_COMMIT_MSG = "${sh(script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()}"
        // Get HEAD commit author
        GIT_AUTHOR = "${sh(script: 'git log -1 --pretty=%cn ${GIT_COMMIT}', returnStdout: true).trim()}"
        // Get HEAD commit email address
        GIT_AUTHOR_EMAIL = "${sh(script: 'git log -1 --pretty=%ae ${GIT_COMMIT}', returnStdout: true).trim()}"
        // Slack channel for notification
        SLACK_CHANNEL = '##zcompute-devops-ci'
        // Integration ticket jira component
        JIRA_COMPONENT = 'asset-api'
    }
    stages {
        // Init
        stage('Initialization') {
            steps {
                script {
                    // Get github organization name
                    env.GIT_ORG = sh(script: "echo $GIT_URL | awk -F/ '{print \$4}'", returnStdout: true).trim()
                    // Get git repository name
                    env.GIT_REPOSITORY = sh(
                        script: "echo $GIT_URL | awk -F/ '{print \$5}' | awk -F. '{print \$1}'",
                        returnStdout: true).trim()
                }
                sh 'printenv'
                // Set build name
                buildName "${env.BUILD_TAG}"
                // Set build description
                buildDescription "${env.GIT_URL} Branch: ${env.GIT_BRANCH} on Worker: ${env.NODE_NAME}"
            }
        }
        // Verify that all new commits are in standard
        stage('Verify commits') {
            when {
                changeRequest()
            }
            steps {
                verifyCommits()
            }
        }
        // Build the build container image
        stage('Build skipper image') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper build $GIT_REPOSITORY-build'
            }
        }
        // Run linters. For example: flake8, pylint, swagger-validate
        stage('Lint') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make lint'
            }
        }
        // Build required packages. For example: go/python packages
        stage('Build packages') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make packages'
            }
        }
        // Generate clients. For example: swagger/hammock clients
        stage('Generate clients') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make clients'
            }
        }
        // This stage will execute unittests
        stage('Unit tests') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make unittest'
            }
        }
        // Create RPM package for this service
        stage('RPM') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make rpm'
            }
        }
        // Build the service image
        stage('Build service image') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make service-image'
            }
        }
        // Run subsystem tests
        stage('Subsystem tests') {
            when {
                changeRequest()
            }
            steps {
                sh 'skipper --build-container-tag $GIT_COMMIT make subsystem'
            }
        }
        // Run clean-build
        stage('Clean build') {
            when {
                anyOf {
                    branch 'master'
                    expression { GIT_BRANCH ==~ /^master_v[0-9\.].+/ }
                }
            }
            steps {
                cleanBuild(
                    env.GIT_REPOSITORY,
                    env.GIT_COMMIT,
                    env.BUILD_TAG,
                    env.GIT_ORG,
                    env.GIT_BRANCH,
                    params.MONKEY_TESTING_FILTER,
                    params.MONKEY_BRANCH,
                    params.ADDITIONAL_MONKEY_PARAMS
                )
            }
        }
        // Run deliver job with the relevant changes
        stage('Deliver') {
            when {
                anyOf {
                    branch 'master'
                    expression { GIT_BRANCH ==~ /^master_v[0-9\.].+/ }
                }
            }
            steps {
                deliver(
                    env.GIT_REPOSITORY,
                    env.GIT_COMMIT,
                    env.JIRA_COMPONENT,
                    env.GIT_AUTHOR_EMAIL,
                    env.BUILD_URL
                )
            }
        }
    }
    // Post steps
    post {
        // Collect junit files
        always {
            junit(
                allowEmptyResults: true,
                testResults: 'reports/*.xml'
            )
            archiveArtifacts(
                allowEmptyArchive: true,
                artifacts: 'logs/*.log, logs/*.stratolog'
            )
        }
        // On every status change
        changed {
            // Notify users using email and slack
            notifyUsers(
                emailAddress: env.GIT_AUTHOR_EMAIL,
                slackChannel: env.SLACK_CHANNEL,
                buildTag: env.BUILD_TAG,
                buildUrl: env.BUILD_URL,
            )
        }
    }
}