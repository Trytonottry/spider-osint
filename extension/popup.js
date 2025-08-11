document.getElementById('scan').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, { action: "get_content" }, (response) => {
    const data = {
      url: tab.url,
      title: tab.title,
      content: response.text.substring(0, 1000),
      target: extractEmail(response.text) || tab.url
    };

    // Отправка в SPIDER API
    fetch('http://localhost:8000/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target: data.target, modules: ['web', 'phishing'] })
    })
    .then(() => alert('Сканирование запущено!'))
    .catch(err => alert('Ошибка: ' + err.message));
  });
});

function extractEmail(text) {
  const match = text.match(/[\w.-]+@[\w.-]+\.\w+/);
  return match ? match[0] : null;
}