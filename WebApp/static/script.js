async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  const log = document.getElementById("log");
  log.innerHTML += "You: " + message + "\n";
  input.value = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let fullResponse = "";

    log.innerHTML += "YASHIKA: ";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      fullResponse += chunk;
      log.innerHTML += chunk;
    }

    log.innerHTML += "\n\n";
  } catch (err) {
    log.innerHTML += "[Error processing command]\n\n";
  }

  log.scrollTop = log.scrollHeight;
}


    const presets = {
      DevModeProtocol: ["Open Chatgpt", "Open Youtube", "Open Vs code"],
    };

    async function runPreset(presetKey) {
      const commands = presets[presetKey];
      for (const cmd of commands) {
        document.getElementById("userInput").value = cmd;
        await sendMessage();
        await new Promise(res => setTimeout(res, 800));
      }
    }

    function toggleSidebar() {
        const sidebar = document.getElementById("sidebar");
        sidebar.classList.toggle("open");
      }

      // Auto-retract sidebar on outside click
  document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');

    // Only close if sidebar is active and click is outside both sidebar and button
    if (
      sidebar.classList.contains('open') &&
      !sidebar.contains(event.target) &&
      !toggleBtn.contains(event.target)
    ) {
      sidebar.classList.remove('open');
    }
  });
