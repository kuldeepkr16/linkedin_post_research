const state = {
  history: [],
  run: null,
  filter: "all",
};

const $ = (selector) => document.querySelector(selector);
const postsEl = $("#posts");
const template = $("#postTemplate");
const runSelect = $("#runSelect");

function formatDate(value) {
  if (!value) return "Unknown time";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Asia/Kolkata",
  }).format(date);
}

function postKey(type, index) {
  const runId = state.run?.generated_at || "unknown";
  return `linkedin-review:${runId}:${type}:${index}`;
}

function getStatus(type, index) {
  return localStorage.getItem(postKey(type, index)) || "unreviewed";
}

function setStatus(type, index, status) {
  const key = postKey(type, index);
  const current = localStorage.getItem(key);
  if (current === status) localStorage.removeItem(key);
  else localStorage.setItem(key, status);
  renderPosts();
}

function titleFor(post, type, index) {
  if (type === "news") return post.source_article || post.key_topic || `News draft ${index + 1}`;
  return post.key_topic || post.concept || `${post.topic || "Concept"} draft ${index + 1}`;
}

function allPosts() {
  if (!state.run) return [];
  const news = (state.run.news_posts || []).map((post, index) => ({ post, type: "news", index }));
  const concepts = (state.run.concept_posts || []).map((post, index) => ({ post, type: "concept", index }));
  return [...news, ...concepts];
}

function renderSummary() {
  const news = state.run?.news_posts?.length || 0;
  const concepts = state.run?.concept_posts?.length || 0;
  $("#totalCount").textContent = news + concepts;
  $("#newsCount").textContent = news;
  $("#conceptCount").textContent = concepts;
  $("#providerName").textContent = state.run?.ai_provider || "unknown";
  $("#generatedAt").textContent = `Generated ${formatDate(state.run?.generated_at)}`;
}

function renderPosts() {
  postsEl.replaceChildren();
  let visible = 0;

  for (const item of allPosts()) {
    const status = getStatus(item.type, item.index);
    if (state.filter !== "all" && state.filter !== item.type && !(state.filter === "ready" && status === "ready")) {
      continue;
    }

    visible += 1;
    const { post, type, index } = item;
    const card = template.content.firstElementChild.cloneNode(true);
    const typeBadge = card.querySelector(".type-badge");
    typeBadge.textContent = type === "news" ? "NEWS" : "CONCEPT";
    typeBadge.classList.add(type);

    card.querySelector(".topic").textContent = post.key_topic || post.topic || "Data Engineering";
    card.querySelector(".post-title").textContent = titleFor(post, type, index);
    card.querySelector(".post-content").textContent = post.post_content || "No post content generated.";

    const reviewBadge = card.querySelector(".review-badge");
    reviewBadge.textContent = status === "ready" ? "Ready to post" : status === "skip" ? "Skipped" : "Unreviewed";
    if (status !== "unreviewed") reviewBadge.classList.add(status);

    const imagePrompt = post.image_prompt || "No image prompt generated for this draft.";
    card.querySelector(".image-prompt").textContent = imagePrompt;

    const source = card.querySelector(".source-link");
    if (type === "news" && post.source_url) source.href = post.source_url;
    else source.hidden = true;

    const copyButton = card.querySelector(".copy-button");
    copyButton.addEventListener("click", async () => {
      await navigator.clipboard.writeText(post.post_content || "");
      const original = copyButton.textContent;
      copyButton.textContent = "Copied";
      setTimeout(() => { copyButton.textContent = original; }, 1200);
    });

    const readyButton = card.querySelector(".ready-button");
    const skipButton = card.querySelector(".skip-button");
    if (status === "ready") readyButton.classList.add("selected");
    if (status === "skip") skipButton.classList.add("selected");
    readyButton.addEventListener("click", () => setStatus(type, index, "ready"));
    skipButton.addEventListener("click", () => setStatus(type, index, "skip"));

    postsEl.append(card);
  }

  $("#emptyState").hidden = visible !== 0;
}

async function loadRun(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`Could not load ${path}: HTTP ${response.status}`);
  state.run = await response.json();
  renderSummary();
  renderPosts();
}

function renderRunPicker() {
  runSelect.replaceChildren();
  for (const run of state.history) {
    const option = document.createElement("option");
    option.value = run.path;
    option.textContent = `${formatDate(run.generated_at)} · ${run.total_count} drafts`;
    runSelect.append(option);
  }
}

async function init() {
  try {
    const response = await fetch("data/history.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`History request failed: HTTP ${response.status}`);
    const history = await response.json();
    state.history = history.runs || [];
    renderRunPicker();

    if (state.history.length) await loadRun(state.history[0].path);
    else await loadRun("data/latest.json");
  } catch (error) {
    postsEl.innerHTML = `<div class="empty">Dashboard data could not be loaded. ${error.message}</div>`;
  }
}

runSelect.addEventListener("change", () => loadRun(runSelect.value));

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filter").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    state.filter = button.dataset.filter;
    renderPosts();
  });
});

init();
