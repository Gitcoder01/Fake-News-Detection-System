const analyzeButton = document.getElementById("analyzeBtn");

const statusText = document.getElementById("status");

const resultCard = document.getElementById("resultCard");

const resultText = document.getElementById("result");

const confidenceText = document.getElementById("confidence");

const progressBar = document.getElementById("progressBar");

const wordsSection = document.getElementById("wordsSection");

const wordsList = document.getElementById("words");


analyzeButton.addEventListener("click", async () => {

    // Reset interface

    resultCard.style.display = "none";

    wordsSection.style.display = "none";

    statusText.textContent = "Analyzing article...";

    analyzeButton.disabled = true;

    analyzeButton.textContent = "⏳ Analyzing...";

    try {

        // Get current tab

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        // Make sure a tab exists

        if (!tab || !tab.id) {

            throw new Error("No active tab found.");

        }

        // Extract article text

        chrome.tabs.sendMessage(
            tab.id,
            { action: "extractText" },

            async (response) => {

                // Check Chrome runtime error

                if (chrome.runtime.lastError) {

                    statusText.textContent =
                        "Unable to read this page.";

                    resetButton();

                    return;
                }

                // Check extracted text

                if (!response || !response.text) {

                    statusText.textContent =
                        "Unable to read page.";

                    resetButton();

                    return;
                }

                try {

                    // Send article to Flask

                    const apiResponse = await fetch(
                        "http://127.0.0.1:5000/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type": "application/json"
                            },

                            body: JSON.stringify({
                                text: response.text
                            })
                        }
                    );

                    // Check API response

                    if (!apiResponse.ok) {

                        const errorText =
                            await apiResponse.text();

                        console.error(
                            "Flask API error:",
                            errorText
                        );

                        statusText.textContent =
                            "API error: " +
                            apiResponse.status;

                        resetButton();

                        return;
                    }

                    // Convert response to JSON

                    const result =
                        await apiResponse.json();

                    // Display result

                    displayResult(result);

                    // Reset button

                    resetButton();

                } catch (error) {

                    console.error(
                        "API connection error:",
                        error
                    );

                    statusText.textContent =
                        "Cannot connect to Flask API.";

                    resetButton();

                }

            }
        );

    } catch (error) {

        console.error(
            "Extension error:",
            error
        );

        statusText.textContent =
            "Something went wrong.";

        resetButton();

    }

});


/* DISPLAY RESULT */

function displayResult(result) {

    const prediction = result.prediction;

    const confidence = Number(result.confidence);

    // Remove status message

    statusText.textContent = "";

    // Show result card

    resultCard.style.display = "block";

    // Prediction text

    resultText.textContent = prediction;

    // Confidence

    confidenceText.textContent =
        "Confidence: " + confidence + "%";

    // Confidence bar

    progressBar.style.width =
        confidence + "%";

    // Prediction-specific styling

    if (prediction === "Real News") {

        resultText.style.color = "#15803d";

        progressBar.style.background =
            "#22c55e";

    } else {

        resultText.style.color = "#dc2626";

        progressBar.style.background =
            "#ef4444";

    }

    // Display important words

    displayImportantWords(
        result.important_words
    );

}


/* DISPLAY IMPORTANT WORDS */

function displayImportantWords(words) {

    wordsList.innerHTML = "";

    if (!words || words.length === 0) {

        wordsSection.style.display = "none";

        return;
    }

    wordsSection.style.display = "block";

    words.forEach(item => {

        const li = document.createElement("li");

        const word = document.createElement("span");

        word.className = "word-name";

        word.textContent = item.word;

        const weight = document.createElement("span");

        weight.className = "word-weight";

        const sign =
            item.weight >= 0 ? "+" : "";

        weight.textContent =
            sign + item.weight;

        li.appendChild(word);

        li.appendChild(weight);

        wordsList.appendChild(li);

    });

}

/* RESET BUTTON */

function resetButton() {

    analyzeButton.disabled = false;

    analyzeButton.textContent =
        "🔍 Analyze Current Page";

}
