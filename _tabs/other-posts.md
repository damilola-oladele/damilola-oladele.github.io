---
# the default layout is 'page'
icon: fas fa-archive
order: 4
---
<style>
.card-container {
display: grid;
grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
gap: 16px;
margin-top: 20px;
}
.card {
background: inherit;
border-radius: 12px;
box-shadow: 0 4px 8px rgba(25, 24, 24, 0.08);
padding: 20px;
transition: transform 0.2s, box-shadow 0.2s;
border-color: #363639ff;
}
.card:hover {
transform: translateY(-5px);
box-shadow: 0 8px 16px rgba(43, 39, 39, 0.12);
}
.card a {
text-decoration: none;
font-weight: bold;
color: #2563eb;
}
.card a:hover {
text-decoration: underline;
}
#searchBoxArticles {
margin-bottom: 20px;
padding: 10px;
width: 100%;
max-width: 400px;
border: 1px solid #ccc;
border-radius: 8px;
}
</style>
<input type="text" id="searchBoxArticles" placeholder="Search posts...">
<div class="card-container" id="articles">
<div class="card">
<a href="https://wagtail.org/blog/our-first-google-season-of-docs-2023/" target="_blank">
Meet Damilola Oladele, Our First Technical Writer for Google Season of Docs
</a>
</div>
<div class="card">
<a href="https://wagtail.org/blog/progress-report-on-the-google-season-of-docs-for-the-month-of-june/" target="_blank">
My progress in June for Google Season of Docs 2023
</a>
</div>
<div class="card"><a href="https://wagtail.org/blog/a-new-tutorial-series-for-the-new-year/" target="_blank">A new tutorial series for the new year</a></div>
<div class="card"><a href="https://wagtail.org/blog/the-lessons-i-learned-during-my-google-season-of-docs-program/" target="_blank">The lessons I learned during my Google Season of Docs program</a></div>
<div class="card">
<a href="https://www.freecodecamp.org/news/objects-in-javascript-for-beginners/" target="_blank">
Objects in JavaScript – A Beginner's Guide
</a>
</div>
<div class="card"><a href="https://www.freecodecamp.org/news/how-to-create-a-csv-file-in-python/" target="_blank">How to Create a CSV File Using Python</a></div>
<div class="card"><a href="https://wordsmith0x.substack.com/p/a-step-by-step-guide-to-earning-crypto" target="_blank">A step-by-step guide to earning crypto by yapping</a></div>
<div class="card"><a href="https://wordsmith0x.substack.com/p/what-is-yapping" target="_blank">What is yapping in crypto?</a></div>
</div>
<script>
document.addEventListener('DOMContentLoaded', () => {
const filterCards = (containerId, query) => {
const container = document.getElementById(containerId);
const cards = container.getElementsByClassName('card');
const filter = query.toLowerCase();
Array.from(cards).forEach(card => {
const text = card.innerText.toLowerCase();
card.style.display = text.includes(filter) ? "block" : "none";
});
};
const searchBoxes = document.querySelectorAll('input[type="text"]');
searchBoxes.forEach(box => {
const containerId = box.id.replace('searchBox', '').toLowerCase();
if (containerId === '') {
box.addEventListener('input', (event) => filterCards('projects', event.target.value));
} else {
box.addEventListener('input', (event) => filterCards(containerId, event.target.value));
}
});
});
</script>