<script>
const unsplashQueries = {{ case.unsplash_queries | tojson if case and case.unsplash_queries else '{}' }};
const sections = ["story", "investigation", "rumors", "suspects", "timeline", "impact"];
const unsplashAccessKey = "YOUR_UNSPLASH_ACCESS_KEY"; // 🔑 Replace this with your actual Unsplash key

// -----------------------------
// Load page + data rendering
// -----------------------------
window.addEventListener('load', () => {
    const caseExists = window.caseExists;
    const details = window.details;
    const reviews = window.reviews;
    const redditLinks = window.redditLinks;
    const gallery = window.gallery;

    if (caseExists) {
        // MAP
        if (details.location && details.location.lat && details.location.lng) {
            const map = L.map('map', { scrollWheelZoom: false })
                        .setView([details.location.lat, details.location.lng], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
            L.marker([details.location.lat, details.location.lng]).addTo(map);
        }

        // EVIDENCE
        const evidenceList = document.getElementById('evidence-list');
        if (evidenceList && details.evidence) {
            evidenceList.innerHTML = '';
            details.evidence.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                evidenceList.appendChild(li);
            });
        }

        // REVIEWS
        const reviewList = document.getElementById('review-list');
        if (reviewList && reviews) {
            reviewList.innerHTML = '';
            reviews.forEach(r => {
                const li = document.createElement('li');
                li.innerHTML = `<b>${r.user}:</b> ${r.text}`;
                reviewList.appendChild(li);
            });
        }

        // REDDIT LINKS
        const redditList = document.getElementById('reddit-list');
        if (redditList && redditLinks) {
            redditList.innerHTML = '';
            redditLinks.forEach(r => {
                const li = document.createElement('li');
                li.innerHTML = `<a href="${r.url}" target="_blank">${r.title}</a>`;
                redditList.appendChild(li);
            });
        }

        // GALLERY
        const galleryDiv = document.getElementById('gallery');
        if (galleryDiv && gallery) {
            galleryDiv.innerHTML = '';
            gallery.forEach(imgUrl => {
                const img = document.createElement('img');
                img.src = imgUrl;
                img.width = 250;
                img.alt = "Case Image";
                galleryDiv.appendChild(img);
            });
        }

        // PDF BUTTON
        const pdfBtn = document.getElementById('download-pdf');
        if (pdfBtn) {
            pdfBtn.addEventListener('click', () => {
                window.location.href = window.pdfUrl;
            });
        }
    }

    // -----------------------------
    // Fetch Unsplash images per section
    // -----------------------------
    loadUnsplashImages();
});

// -----------------------------
// Unsplash image loader
// -----------------------------
async function loadUnsplashImages() {
    for (const sec of sections) {
        const q = unsplashQueries[sec];
        if (!q) continue;

        try {
            const res = await fetch(`https://api.unsplash.com/photos/random?query=${encodeURIComponent(q)}&client_id=${unsplashAccessKey}`);
            const data = await res.json();
            const img = document.getElementById(`img-${sec}`);
            if (img && data.urls && data.urls.regular) {
                img.src = data.urls.regular;
            }
        } catch (err) {
            console.error("Unsplash fetch error for", sec, err);
        }
    }
}
</script>
