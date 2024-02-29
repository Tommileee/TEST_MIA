// PM2 Configuration
module.exports = {
  apps: [{
    name: "message-broker",
    script: "./services/message_broker.py",
    interpreter: "venv/bin/python"
  },
  {
    name: "camera_service",
    script: "./services/camera_service.py",
    interpreter: "venv/bin/python"
  },
  {
    name: "webserver",
    script: "./services/webserver.py",
    interpreter: "venv/bin/python"
  },
  {
    name: "tts",
    script: "./services/tts.py",
    interpreter: "venv/bin/python"
  },
  {
    name: "network-monitor",
    script: "./scripts/monitor_network.sh",
    interpreter: "bash"
  }]
}
