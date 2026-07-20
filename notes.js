/**
 * =====================================================================
 * SMARTEDUX - REAL PRODUCTION AI CORE ENGINE INTEGRATION
 * =====================================================================
 */

window.generateNotes = async function() {
    console.log("[SmartEduX Core]: Real API Connection Initiated.");

    const youtubeInput = document.getElementById("ytLink");
    const loadingLoader = document.getElementById("loading");
    const notesOutputBox = document.getElementById("notesOutput");
    const notesTextArea = document.getElementById("notesText");
    const errorBox = document.getElementById("errorBox");

    const urlValue = youtubeInput ? youtubeInput.value.trim() : "";

    if (!urlValue) {
        alert("Please paste a valid YouTube link!");
        return;
    }

    // Reset layout states cleanly
    if (errorBox) {
        errorBox.innerText = "";
        errorBox.classList.add("hidden");
    }
    if (loadingLoader) loadingLoader.classList.remove("hidden");
    if (notesOutputBox) notesOutputBox.classList.add("hidden");

    try {
        // Local storage se active JWT access token uthana
        const token = localStorage.getItem("authToken");

        if (!token) {
            throw new Error("User session expired or unauthorized. Please log in again.");
        }

        // ASLI BACKEND HIT LOCK WITH SECURE JWT AUTHORIZATION HEADER
        const response = await fetch('http://127.0.0.1:8000/api/notes/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Secure token attached!
            },
            body: JSON.stringify({ youtube_url: urlValue })
        });

        const data = await response.json();

        if (data.status === 'success') {
            if (loadingLoader) loadingLoader.classList.add("hidden");
            if (notesOutputBox) notesOutputBox.classList.remove("hidden");

            // 1. Render Real Markdown Notes dynamically
            if (notesTextArea) {
                notesTextArea.innerHTML = marked.parse(data.summary);
            }

            // 2. Remove any old quiz box if existing
            let oldQuizBox = document.getElementById("dynamic-quiz-box");
            if (oldQuizBox) oldQuizBox.remove();

            // 3. Create and Build Real Quiz Section
            const dynamicQuizBox = document.createElement("div");
            dynamicQuizBox.id = "dynamic-quiz-box";
            dynamicQuizBox.className = "mt-8 pt-6 border-t border-gray-300 text-left";
            dynamicQuizBox.innerHTML = "<h4 class='text-2xl font-bold text-[#0b2149] mb-4'>🎯 AI Generated Quiz (5 MCQs)</h4>";

            if (data.quiz && data.quiz.length > 0) {
                data.quiz.forEach((q, index) => {
                    dynamicQuizBox.innerHTML += `
                        <div class="mb-5 p-4 bg-white rounded-lg border border-gray-200 shadow-sm animate-fadeInUp">
                            <p class="font-bold text-gray-900 mb-2">Q${index + 1}: ${q.question}</p>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-700">
                                <label class="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer"><input type="radio" name="q${index}" value="A"> A) ${q.options.A}</label>
                                <label class="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer"><input type="radio" name="q${index}" value="B"> B) ${q.options.B}</label>
                                <label class="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer"><input type="radio" name="q${index}" value="C"> C) ${q.options.C}</label>
                                <label class="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer"><input type="radio" name="q${index}" value="D"> D) ${q.options.D}</label>
                            </div>
                        </div>`;
                });
            } else {
                dynamicQuizBox.innerHTML += "<p class='text-gray-500 text-sm pl-2'>No quiz items returned from stream core.</p>";
            }

            if (notesOutputBox) {
                notesOutputBox.insertBefore(dynamicQuizBox, notesOutputBox.lastElementChild);
            }

        } else {
            throw new Error(data.error || "Failed to compile notes from Gemini stream.");
        }

    } catch (err) {
        console.error("[CRITICAL FRONTEND FAULT]:", err);
        if (loadingLoader) loadingLoader.classList.add("hidden");
        if (errorBox) {
            errorBox.innerText = `API Operational Failure: ${err.message}`;
            errorBox.classList.remove("hidden");
        }
    }
}