chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "get_content") {
    const text = document.body.innerText;
    sendResponse({ text });
  }
});