    document.getElementById("analyzeBtn").addEventListener("click", async () => {

    const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
    });

    chrome.tabs.sendMessage(
    tab.id,
    { action: "extractText" },
    async (response) => {

        if (!response || !response.text) {

            document.getElementById("result").textContent =
                "Unable to read page.";

            return;
        }

        try {

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

            const result = await apiResponse.json();

            document.getElementById("result").textContent =
                "Prediction: " + result.prediction;

            document.getElementById("confidence").textContent =
                "Confidence: " + result.confidence + "%";

            const list = document.getElementById("words");

            list.innerHTML = "";

            result.important_words.forEach(item => {

                const li = document.createElement("li");

                li.textContent =
                    item.word + " (" + item.weight + ")";

                list.appendChild(li);

            });

        } catch (error) {

            document.getElementById("result").textContent =
                "Cannot connect to Flask API.";

            console.error(error);

        }

    }
    );

    });