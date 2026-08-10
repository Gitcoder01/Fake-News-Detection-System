// Function to extract the main article text
function getPageContent() {

    // Try common article containers first
    const selectors = [
        "article",
        "main",
        "[role='main']",
        ".article-body",
        ".article-content",
        ".story-body",
        ".post-content",
        ".entry-content"
    ];

    for (const selector of selectors) {
        const element = document.querySelector(selector);

        if (element && element.innerText.trim().length > 300) {
            return element.innerText;
        }
    }

    // Fall back to the entire page
    return document.body.innerText;
}

// Listen for requests from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    if (request.action === "extractText") {

        const text = getPageContent();

        sendResponse({
            text: text
        });

    }

    return true;
});