document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/upload/", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    alert(data.status);
});

async function summarize() {
    const topic = document.getElementById("topic").value;
    if (!topic) return alert("Enter a topic");

    const response = await fetch(`/summarize/?topic=${encodeURIComponent(topic)}`);
    const data = await response.json();
    document.getElementById("summary").innerText = data.summary;
}
