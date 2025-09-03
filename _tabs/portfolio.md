---
# the default layout is 'page'
icon: fas fa-pen
order: 2
image:
  path: /assets/img/favicons/android-chrome-512x512.png
  alt: Damilola Oladele's headshot
---
<style>
h2 {
margin-top: 40px;
color: #7f8186ff;
}
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
.card-footer {
margin-top: 15px;
display: flex;
justify-content: space-between;
align-items: center;
}
.learn-more-btn {
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
border: none;
padding: 8px 16px;
border-radius: 6px;
cursor: pointer;
font-size: 14px;
font-weight: 500;
transition: all 0.3s ease;
box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.learn-more-btn:hover {
transform: translateY(-2px);
box-shadow: 0 4px 8px rgba(0,0,0,0.2);
background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}
#searchBox, #searchBoxSpeaking, #searchBoxArticles {
margin-bottom: 20px;
padding: 10px;
width: 100%;
max-width: 400px;
border: 1px solid #ccc;
border-radius: 8px;
}
.speaking-heading {
text-decoration: none;
font-weight: bold;
color: #2563eb;
border-bottom: 1px solid #333;
}
.speaking-txt {
color: #7f8186ff;
}
.modal {
display: none;
position: fixed;
z-index: 1000;
left: 0;
top: 0;
width: 100%;
height: 100%;
background-color: rgba(0, 0, 0, 0.5);
backdrop-filter: blur(5px);
opacity: 0;
transition: opacity 0.3s ease;
}
.modal[style*="block"] {
opacity: 1;
}
.modal-content {
margin: 5% auto;
padding: 0;
border-radius: 16px;
width: 90%;
max-width: 800px;
max-height: 85vh;
overflow-y: auto;
box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
animation: modalSlideIn 0.3s ease-out;
transform: translateY(-50px);
transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}
.modal[style*="block"] .modal-content {
transform: translateY(0);
opacity: 1;
}
@keyframes modalSlideIn {
from {
opacity: 0;
transform: translateY(-50px);
}
to {
opacity: 1;
transform: translateY(0);
}
}
.modal-header {
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
padding: 25px 30px;
border-radius: 16px 16px 0 0;
display: flex;
justify-content: space-between;
align-items: center;
}
.modal-title {
font-size: 24px;
font-weight: 600;
margin: 0;
color: white;
}
.close {
color: white;
font-size: 32px;
font-weight: bold;
cursor: pointer;
transition: all 0.2s ease;
line-height: 1;
}
.close:hover {
color: #f0f0f0;
transform: scale(1.1);
}
.modal-body {
padding: 30px;
background: #fff;
}
.modal-section {
margin-bottom: 30px;
}
.modal-section:last-child {
margin-bottom: 0;
}
.modal-section h3 {
color: #333;
font-size: 20px;
margin-bottom: 15px;
padding-bottom: 8px;
border-bottom: 2px solid #667eea;
display: inline-block;
}
.modal-section p {
line-height: 1.6;
color: #555;
margin-bottom: 15px;
}
.modal-section a {
color: #2563eb;
text-decoration: none;
font-weight: 500;
}
.modal-section a:hover {
text-decoration: underline;
color: #1d4ed8;
}
@media (max-width: 600px) {
.modal-content {
margin: 10% auto;
width: 95%;
}
.modal-header {
padding: 20px;
}
.modal-title {
font-size: 20px;
}
.modal-body {
padding: 20px;
}
.card-footer {
flex-direction: column;
gap: 10px;
}
}
</style>
<h2>Project / Documentation Work</h2>
<input type="text" id="searchBox" placeholder="Search projects...">
<div class="card-container" id="projects">
<div class="card">
<a href="https://django-otp-webauthn.readthedocs.io/en/latest/" target="_blank">Django OTP WebAuthn documentation</a>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="django-otp-modal">Learn more</button>
</div>
</div>
<div class="card">
<a href="https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/" target="_blank">Ubuntu Packaging Guide</a>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="ubuntu-guide-modal">Learn more</button>
</div>
</div>
<div class="card">
<a href="https://github.com/BlackPythonDevs/blackpythondevs" target="_blank">Black Python Devs Maintainers Guide</a>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="bpd-modal">Learn more</button>
</div>
</div>
<div class="card">
<a href="https://docs.wagtail.org/en/stable/getting_started/index.html" target="_blank">Wagtail Developer Documentation</a>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="wagtail-dev-modal">Learn more</button>
</div>
</div>
<div class="card">
<a href="https://guide.wagtail.org/en-latest/" target="_blank">Wagtail Editors Guide</a>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="wagtail-editor-modal">Learn more</button>
</div>
</div>
<div class="card">
<a href="https://github.com/canonical/open-documentation-academy/issues?q=is%3Aissue%20state%3Aclosed%20assignee%3Aactivus-d" target="_blank">Canonical’s Open Documentation Academy (CODA) Contributions</a>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="coda-modal">Learn more</button>
</div>
</div>
</div>
<h2>Public Speaking and Content</h2>
<input type="text" id="searchBoxSpeaking" placeholder="Search ...">
<div class="card-container" id="speaking">
<div class="card">
<p class="speaking-heading">Terntribe Contributors' Corner</p>
<p class="speaking-txt">In-person speaking engagement</p>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="terntribe-modal">Learn more</button>
</div>
</div>
<div class="card">
<p class="speaking-heading">Freelance Coalition for Developing Countries (FCDC)</p>
<p class="speaking-txt">Guest speaker</p>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="fcdc-modal">Learn more</button>
</div>
</div>
<div class="card">
<p class="speaking-heading">DocumentWrite Twitter Spaces</p>
<p class="speaking-txt">Series host and presenter</p>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="documentwrite-modal">Learn more</button>
</div>
</div>
<div class="card">
<a href="https://www.youtube.com/@damilola_oladele" target="_blank">YouTube Content Creation</a>
<p class="speaking-txt">Channel: damilola_oladele</p>
<div class="card-footer">
<button class="learn-more-btn" data-modal-id="youtube-modal">Learn more</button>
</div>
</div>
</div>
<h2>Articles</h2>
<input type="text" id="searchBoxArticles" placeholder="Search articles...">
<div class="card-container" id="articles">
<div class="card"><a href="https://damilola-oladele.github.io/posts/get_started_with_lxc/" target="_blank">Get started with LXC</a></div>
<div class="card"><a href="https://damilola-oladele.github.io/posts/documentation-experience-in-open-source/" target="_blank">Why gaining documentation experience in open source is hard</a></div>
<div class="card"><a href="https://www.freecodecamp.org/news/what-is-the-dom-explained-in-plain-english/" target="_blank">What is the DOM? The Document Object Model Explained in Plain English</a></div>
<div class="card"><a href="https://www.freecodecamp.org/news/how-to-use-oop-in-python/" target="_blank">How to Use OOP in Python</a></div>
<div class="card"><a href="https://www.freecodecamp.org/news/django-model-relationships/" target="_blank">How to Define Relationships Between Django Models</a></div>
<div class="card"><a href="https://www.freecodecamp.org/news/how-to-stay-motivated-while-learning-to-code/" target="_blank">How to Stay Motivated While Learning to Code</a></div>
<div class="card"><a href="https://damilola-oladele.github.io/posts/the-blockchain-trilemma-challenge/" target="_blank">The blockchain trilemma challenge</a></div>
<div class="card"><a href="https://damilola-oladele.github.io/posts/what-are-smart-contracts-on-blockchain/" target="_blank">What are smart contracts on blockchain?</a></div>
<div class="card"><a href="https://damilola-oladele.github.io/posts/juno-bringing-decentralization-to-starknet/" target="_blank">Juno: Bringing decentralization to Starknet</a></div>
<div class="card"><a href="https://wagtail.org/blog/the-lessons-i-learned-during-my-google-season-of-docs-program/" target="_blank">The lessons I learned during my Google Season of Docs program</a></div>
</div>
<!-- Modals -->
<div id="django-otp-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Django OTP WebAuthn Documentation</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>About the Project</h3>
<p><a href="https://django-otp-webauthn.readthedocs.io/en/latest/" target="_blank">Django OTP WebAuthn</a> is an implementation of WebAuthn Passkeys for Django applications. It extends the django-otp framework to support multi-factor authentication using passkeys.</p>
<p>Django OTP WebAuthn simplifies passkey authentication by handling all cryptographic operations through py_webauthn.</p>
</div>
<div class="modal-section">
<h3>Work Done</h3>
<p>Built the project’s documentation from scratch, starting with only the README as a reference. To better understand the project’s direction, I held an in-depth discussion with the project owner about its goals and intended audience. I authored all sections, deployed the documentation, and continue to maintain it as a go-to resource for developers integrating passkeys into Django projects, as well as for new contributors navigating the codebase.</p>
</div>
</div>
</div>
</div>
<div id="wagtail-dev-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Wagtail Developer Documentation</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>About the Project</h3>
<p>The <a href="https://docs.wagtail.org/en/stable/index.html" target="_blank">Wagtail developer documentation</a> is the main guide for developers who want to build and customize Wagtail CMS sites. It explains how to set up Wagtail, change its settings, create content types, design page layouts, add new features, and everything else developers need to make Wagtail sites.</p>
</div>
<div class="modal-section">
<h3>Work Done</h3>
<p>I reviewed and improved the <a href="https://docs.wagtail.org/en/stable/getting_started/index.html" target="_blank">Getting Started</a> section of the documentation. I noticed that while the section explained enough Wagtail features, it needed more background for new users who did not know Django. So, I added a new introduction page for beginners who are new to Wagtail. I also changed the order so that the <a href="https://docs.wagtail.org/en/stable/getting_started/tutorial.html" target="_blank">Getting Started tutorial</a> comes right after the introduction. I made the tutorial better by listing what you need to know before starting and by adding clear comments to the code examples.</p>
<p>Second, I authored a new <a href="https://docs.wagtail.org/en/latest/tutorial/index.html#" target="_blank">tutorial series</a> to aid the onboarding of new developers. The tutorial takes users through a journey of converting the blog site they built with the Wagtail getting started tutorial into a fully deployable portfolio site. One important part of the tutorial is the deployment section. Deployment is one aspect that's usually a pain point for new and existing Wagtail users. The tutorial provides a deployment option, which they can use in their subsequent Wagtail projects. You can get more information about the different Wagtail features covered in the tutorial <a href="https://wagtail.org/blog/a-new-tutorial-series-for-the-new-year/" target="_blank">here</a>.</p>
</div>
</div>
</div>
</div>
<div id="wagtail-editor-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Wagtail Editor's Guide Documentation</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>About the Project</h3>
<p>The <a href="https://guide.wagtail.org/en-latest/" target="_blank">Wagtail Editor's guide</a> is written for the users of a Wagtail-powered site. That is, the content editors, moderators, and administrators who add, review, and approve content on a day-to-day basis.</p>
</div>
<div class="modal-section">
<h3>Work Done</h3>
<p>First, I researched the choice of a style guide for the documentation and improved its content following the chosen style guide. You can read the report showing the choice of the style guide and the rationale behind its adoption <a href="https://github.com/wagtail/guide/discussions/282#discussioncomment-4332158" target="_blank">here</a>.</p>
<p>Second, I improved the <a href="https://guide.wagtail.org/en-latest/how-to-guides/" target="_blank">How-to guides</a> section by adding nine additional guides.</p>
<p>Third, I authored a new <a href="https://guide.wagtail.org/en-latest/concepts/" target="_blank">Concepts</a> section to explain some Wagtail-specific terminologies. The new Concepts section provides editors with enough context to aid their usage of the documentation and the Wagtail admin interface.</p>
<p>Finally, I suggested the replacement of the existing Tutorial section with a Getting started section. This was after deliberating with the Wagtail core engineers working with me on the project. We arrived at the decision because the section doesn't actually contain a tutorial, and writing a tutorial where users can quickly learn to use the CMS will require users to be able to set up the Wagtail <a href="https://github.com/wagtail/bakerydemo" target="_blank">bakerydemo</a> on their local machine. To set up the Wagtail bakerydemo, users need to have some basic programming experience. This would be a difficult prerequisite for learning since most editors using the Wagtail admin interface have a non-technical background. The new Getting started section has an <a href="https://guide.wagtail.org/en-latest/getting-started/overview/" target="_blank">overview</a> that introduces the editors to what Wagtail is and what to expect from using the documentation. This sets the tone for adding more content to the section in the future.</p>
</div>
</div>
</div>
</div>
<div id="coda-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Canonical’s Open Documentation Academy (CODA) Contributions</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>About the Project</h3>
<p><a href="https://documentationacademy.org/" target="_blank">CODA</a> is a collaboration between Canonical’s documentation team and documentation newcomers, experts, and those in-between. Its goal is to help us all improve documentation, become better writers, and grow as open source contributors.</p>
</div>
<div class="modal-section">
<h3>Work Done</h3>
<p>Made several contributions through CODA across multiple Canonical projects, including the Public Cloud docs, Ubuntu Server docs, LXD docs, Scapcraft docs, and adding articles to the CODA website. You can view my contributions <a href="https://github.com/canonical/open-documentation-academy/issues?q=is%3Aissue%20state%3Aclosed%20assignee%3Aactivus-d" target="_blank">here</a>.</p>
</div>
</div>
</div>
</div>
<div id="ubuntu-guide-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Ubuntu Packaging Guide</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>About the Project</h3>
<p>The <a href="https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/" target="_blank">Ubuntu Packaging Guide</a> is the official resource for learning Ubuntu development and packaging. It covers the key players, processes, and tools, helps you set up your development environment, shows you how to join the community, and guides you through fixing an Ubuntu bug.</p>
</div>
<div class="modal-section">
<h3>Work Done</h3>
<p>I improved the Ubuntu Packaging Guide by authoring docs that addresses knowledge gaps for  developers.</p>
<p>I authored a new <a href="https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/how-to/propose-changes/" target="_blank">how-to guide that provides step-by-step instructions for proposing changes to Ubuntu packages</a>. The guide serves new and experienced contributors and walks them through finding problems, obtaining code, developing solutions, testing fixes, pushing changes to Launchpad, and requesting reviews and merges.</p>
<p>I authored <a href="https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/reference/debian-policy/" target="_blank">reference documentation on Debian Policy</a> and its relationship to the Standards-Version field in debian/control. The documentation includes a policy summary, explanations of the Standards-Version field's format and compliance tracking role, and an upgrade checklist. This work addresses package maintainers' needs for policy compliance links and Standards-Version update guidance while helping new maintainers understand the connection between Standards-Version and Debian Policy.</p>
<p>I introduced a <a href="https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/reference/filesystem-hierarchy-standard/" target="_blank">reference documentation on the Linux Filesystem Hierarchy Standard (FHS)</a> that helps new Ubuntu developers understand file installation locations during packaging. The reference explains key filesystem locations' purposes and structures, prescribes required directories and their roles, and provides a framework for separating shareable from unshareable files and static from variable files. FHS compliance ensures developers and system administrators can predict file locations, and the documentation conforms to FHS 3.0 specifications while covering packaging-relevant portions.</p>
<p>I authored the <a href="https://github.com/canonical/ubuntu-packaging-guide/pull/69" target="_blank">documentation on SRU (Stable Release Updates)</a> that details how the SRU  process ensures vetting and testing of changes to stable releases. The process protects users  who depend on stable releases for daily operations from disruptive problems.</p>
<p>I authored the <a href="https://github.com/canonical/ubuntu-packaging-guide/pull/75" target="_blank">documentation on Sponsorship</a> that clarifies how developers without upload rights can submit patches and new packages for review. Authorized developers upload approved changes on their behalf through this process.</p>
</div>
</div>
</div>
</div>
<div id="bpd-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Black Python Devs Maintainers Guide</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>About the Project</h3>
<p>The <a href="https://github.com/BlackPythonDevs/blackpythondevs" target="_blank">Black Python Devs Maintainers Guide</a> is an open-source repository that documents the Black Python Devs community programs, policies, roles, and responsibilities. The guide ensures transparency in how the community operates and makes decisions.</p>
</div>
<div class="modal-section">
<h3>Work Done</h3>
<p>I own and maintain the Black Python Devs Maintainers Guide, where I organized documentation for the community’s programs, policies, and roles. I led a volunteer team to author content and develop a <a href="https://github.com/BlackPythonDevs/blackpythondevs/blob/main/style_guide.md" target="_blank">style guide</a> with an editorial process that cut review time, improved clarity, and made the docs easier to adopt across similar Python organizations.</p>
</div>
</div>
</div>
</div>
<div id="terntribe-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Terntribe Contributors’ Corner</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>In-person speaking engagement</h3>
<p>Presented on open source misconceptions in African innovation context.</p>
<p>Discussed strategies for government, NGO, and educational support of open source initiatives.</p>
</div>
</div>
</div>
</div>
<div id="documentwrite-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">DocumentWrite Twitter Spaces</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>Series Host and Presenter</h3>
<p>Hosted multiple sessions on technical writing and developer relations topics.</p>
<p>Covered conference attendance strategies, career development, global audience writing, and DevRel vs. technical writing.</p>
<p>Presented on social media navigation for technical writers and soft skills development.</p>
</div>
</div>
</div>
</div>
<div id="fcdc-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">Freelance Coalition for Developing Countries (FCDC)</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>Guest Speaker</h3>
<p>Delivered presentation on breaking into technical writing without formal background.</p>
<p>Discussed skills required for technical writing success and content creation strategies.</p>
<p>Provided insights on monetizing technical writing skills for BIPOC freelancers.</p>
<p><strong>Recording available:<a href="https://x.com/i/spaces/1BRJjZwkAXaJw/peek?s=20" target="_blank">Twitter Spaces session</a>.</strong></p>
</div>
</div>
</div>
</div>
<div id="youtube-modal" class="modal">
<div class="modal-content">
<div class="modal-header">
<h2 class="modal-title">YouTube Content Creation</h2>
<span class="close">&times;</span>
</div>
<div class="modal-body">
<div class="modal-section">
<h3>Channel: <a href="https://www.youtube.com/@damilola_oladele" target="_blank">damilola_oladele</a></h3>
<p>Created video tutorials on ReactJS concepts and programming fundamentals.</p>
<p>Produced educational content for developer audiences.</p>
</div>
</div>
</div>
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
const openModal = (modalId) => {
const modal = document.getElementById(modalId);
if (modal) {
modal.style.display = "block";
document.body.style.overflow = "hidden";
void modal.offsetHeight;
}
};
const closeModal = (modalId) => {
const modal = document.getElementById(modalId);
if (modal) {
modal.style.display = "none";
document.body.style.overflow = "auto";
}
};
const learnMoreButtons = document.querySelectorAll('.learn-more-btn');
learnMoreButtons.forEach(button => {
button.addEventListener('click', () => {
const modalId = button.getAttribute('data-modal-id');
if (modalId) {
openModal(modalId);
}
});
});
const closeButtons = document.querySelectorAll('.modal .close');
closeButtons.forEach(button => {
button.addEventListener('click', () => {
const modal = button.closest('.modal');
if (modal) {
closeModal(modal.id);
}
});
});
window.addEventListener('click', (event) => {
const modals = document.getElementsByClassName('modal');
Array.from(modals).forEach(modal => {
if (event.target === modal && modal.style.display === "block") {
closeModal(modal.id);
}
});
});
document.addEventListener('keydown', (event) => {
if (event.key === 'Escape') {
const modals = document.getElementsByClassName('modal');
Array.from(modals).forEach(modal => {
if (modal.style.display === "block") {
closeModal(modal.id);
}
});
}
});
});
</script>
