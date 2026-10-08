// Extract the main article text from the current webpage
function getPageContent() {

    // Remove elements that are usually not part of the article
    const unwantedSelectors = [
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "aside",
        "form",
        "iframe",
        ".advertisement",
        ".ads",
        ".ad",
        ".sidebar",
        ".comments",
        ".social-share",
        ".newsletter"
    ];

    unwantedSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(element => {
            element.remove();
        });
    });

    // Common article containers
    const selectors = [
        "article",
        "[role='article']",
        "main article",
        "main",
        "[role='main']",
        ".article-body",
        ".article-content",
        ".story-body",
        ".story-content",
        ".post-content",
        ".entry-content",
        ".article__body",
        ".article-text",
        ".story-text"
    ];

    // Try to find the main article
    for (const selector of selectors) {

        const element = document.querySelector(selector);

        if (element) {

            const text = element.innerText.trim();

            // Only accept reasonably large blocks of text
            if (text.length > 500) {
                return text;
            }
        }
    }

    // Fallback
    const bodyText = document.body.innerText.trim();

    if (bodyText.length > 500) {
        return bodyText;
    }

    // Nothing useful found
    return "";
}

// Listen for requests from popup
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {

        if (request.action === "extractText") {

            const text = getPageContent();

            sendResponse({
                text: text
            });
        }

        return true;
    }
);