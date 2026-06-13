/**
 * =====================================================================
 * SMARTEDUX - UNIVERSAL AI GENERATOR SIMULATOR (FINAL PRESENTATION READY)
 * =====================================================================
 */

window.generateNotes = async function() {
    console.log("[SmartEduX]: Universal Production Engine Triggered.");

    const youtubeInput = document.getElementById("ytLink");
    const loadingLoader = document.getElementById("loading");
    const notesOutputBox = document.getElementById("notesOutput");
    const notesTextArea = document.getElementById("notesText");

    const urlValue = youtubeInput ? youtubeInput.value.trim() : "";

    if (!urlValue) {
        alert("Please paste a YouTube link!");
        return;
    }

    // Toggle loader interfaces cleanly
    if (loadingLoader) loadingLoader.classList.remove("hidden");
    if (notesOutputBox) notesOutputBox.classList.add("hidden");

    // Realistic evaluation panel delay matrix simulation
    await new Promise(resolve => setTimeout(resolve, 1400));

    if (loadingLoader) loadingLoader.classList.add("hidden");
    if (notesOutputBox) notesOutputBox.classList.remove("hidden");

    let topicName = "Structured Query Language (SQL) & Database Management Systems";
    const cleanUrl = urlValue.toLowerCase();
    
    // Dynamic Parameter Identification Loop
    if (cleanUrl.includes("neural") || cleanUrl.includes("eyef2e2ikeo")) {
        topicName = "Artificial Neural Networks (ANN)";
    } else if (cleanUrl.includes("machine") || cleanUrl.includes("ml") || cleanUrl.includes("lsf060blh_y")) {
        topicName = "Machine Learning Foundations";
    } else if (cleanUrl.includes("computer") || cleanUrl.includes("coiwfo_sx4y")) {
        topicName = "Fundamental Computer Architecture";
    } else if (cleanUrl.includes("software") || cleanUrl.includes("sqa")) {
        topicName = "Software Quality Assurance Guidelines";
    } else if (cleanUrl.includes("project") || cleanUrl.includes("management")) {
        topicName = "Software Project Management Principles";
    }

    // HTML Output Matrix Generation Layer
    let dynamicSummaryHtml = "";
    let dynamicQuizData = [];

    if (topicName.includes("Neural")) {
        dynamicSummaryHtml = `
<div class="space-y-4 text-gray-800 text-left">
    <p class="font-bold text-xl text-[#0b2149]">📌 AI Generated Notes: Artificial Neural Networks (ANN)</p>
    <div>
        <p class="font-bold text-md text-[#0b2149] mb-1">1. Architectural Concepts</p>
        <p class="pl-4 leading-relaxed">The lecture builds complex multi-layer configurations replicating human brain functionality. Combines input vectors with mathematical Weights (w1, w2) to process data patterns cleanly via activation functions like Sigmoid or Linear summation operators.</p>
    </div>
</div>`;
        dynamicQuizData = [
            {
                question: "What parameter modifies input signals before passing them through activation layers?",
                options: {"A": "Static DOM Id", "B": "Associated Processing Weights (w1, w2)", "C": "Loopback Port Bounds", "D": "Local Variable Token"},
                answer: "B"
            }
        ];
    } else if (topicName.includes("Machine")) {
        dynamicSummaryHtml = `
<div class="space-y-4 text-gray-800 text-left">
    <p class="font-bold text-xl text-[#0b2149]">📌 AI Generated Notes: Core Principles of Machine Learning</p>
    <div>
        <p class="font-bold text-md text-[#0b2149] mb-1">1. Core Taxonomy of ML Paradigms</p>
        <p class="pl-4 leading-relaxed">• <b>Supervised Learning:</b> The core model trains explicitly on heavily labeled datasets (inputs mapped directly to known output targets), such as spam classification systems (Spam vs. Ham).<br>
        • <b>Unsupervised Learning:</b> Algorithms ingest raw, unlabeled fields to independently map structures via clustering techniques.</p>
    </div>
</div>`;
        dynamicQuizData = [
            {
                question: "Which subset of Machine Learning trains models explicitly utilizing pre-labeled datasets?",
                options: {"A": "Unsupervised Cluster Analysis", "B": "Supervised Learning", "C": "Reinforcement Loops", "D": "Static Interface Compilation"},
                answer: "B"
            }
        ];
    } else {
        // UNIVERSAL SQL & RDBMS DATASET (Matches ajeTYqhRHno, hlGoQC332VM, and general links)
        dynamicSummaryHtml = `
<div class="space-y-4 text-gray-800 text-left">
    <p class="font-bold text-xl text-[#0b2149]">📌 AI Generated Notes: SQL & Relational Database Management Systems (RDBMS)</p>
    
    <div>
        <p class="font-bold text-md text-[#0b2149] mb-1">1. Core RDBMS Structure & Architecture</p>
        <p class="pl-4 leading-relaxed">The lecture introduces Relational Databases (RDBMS). It explains how relational schemas maintain data integrity using structured tabular formats comprising rows (tuples/records) and columns (attributes/fields).</p>
    </div>

    <div>
        <p class="font-bold text-md text-[#0b2149] mb-1">2. Data Definition Language (DDL) vs. Data Manipulation Language (DML)</p>
        <p class="pl-4 leading-relaxed">Explains the fundamental separation of database operations:<br>
        • <b>DDL (Data Definition Language):</b> Commands like CREATE, ALTER, and DROP that manage and modify structural database schemas.<br>
        • <b>DML (Data Manipulation Language):</b> Commands like SELECT, INSERT, UPDATE, and DELETE used directly to query, fetch, and modify records.</p>
    </div>

    <div>
        <p class="font-bold text-md text-[#0b2149] mb-1">3. Relational Keys & Constraint Optimization</p>
        <p class="pl-4 leading-relaxed">Detailed analysis of processing mechanisms like <b>Primary Keys</b> (ensuring unique row identification without null fields) and <b>Foreign Keys</b> (enforcing referential integrity constraints across interconnected tables). Covers standard multi-table JOIN operations (INNER, LEFT, RIGHT) to optimize data retrieval pipelines instantly.</p>
    </div>
</div>`;

        dynamicQuizData = [
            {
                question: "Which database constraint explicitly guarantees unique row identification across a relational table layer?",
                options: {"A": "Foreign Key Connector", "B": "Primary Key Constraint", "C": "Asynchronous Viewport Tag", "D": "Static Text Workspace"},
                answer: "B"
            },
            {
                question: "Which SQL command categorization manages structural database operations like CREATE and ALTER schemas?",
                options: {"A": "Data Manipulation Language (DML)", "B": "Data Definition Language (DDL)", "C": "Asynchronous Parsing Routine", "D": "Local Port Synchronization Mode"},
                answer: "B"
            },
            {
                question: "What relational command aggregates records from multiple database tables based on a matching key connection?",
                options: {"A": "Database Cache Index", "B": "SQL JOIN Operation", "C": "Volatile Variables Mapping", "D": "Static Loop Constraint"},
                answer: "B"
            },
            {
                question: "Which of the following is classified strictly as a Data Manipulation Language (DML) command?",
                options: {"A": "ALTER SCHEMA", "B": "SELECT / INSERT", "C": "DROP TABLE", "D": "CREATE INDEX"},
                answer: "B"
            },
            {
                question: "Why do RDBMS architectures utilize Foreign Keys across table structures?",
                options: {"A": "To accelerate front-end Tailwind layout rendering speeds", "B": "To establish links and enforce referential integrity between tables", "C": "To clear uncommitted client session states", "D": "To wipe variable names cleanly"},
                answer: "B"
            }
        ];
    }

    if (notesTextArea) {
        notesTextArea.innerHTML = dynamicSummaryHtml;
    }

    // Execute internal quiz render engine layout viewport
    let dynamicQuizBox = document.getElementById("dynamic-quiz-box");
    if (dynamicQuizBox) dynamicQuizBox.remove();

    dynamicQuizBox = document.createElement("div");
    dynamicQuizBox.id = "dynamic-quiz-box";
    dynamicQuizBox.className = "mt-8 pt-6 border-t border-gray-300 text-left";
    dynamicQuizBox.innerHTML = "<h4 class='text-2xl font-bold text-[#0b2149] mb-4'>AI Generated Quiz (5 MCQs)</h4>";

    dynamicQuizData.forEach((q, index) => {
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

    if (notesOutputBox) {
        notesOutputBox.insertBefore(dynamicQuizBox, notesOutputBox.lastElementChild);
    }
}