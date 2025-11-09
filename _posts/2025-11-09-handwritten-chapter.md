---
layout: post
title: "Handwritten Chapter: A Gallery Experiment"
date: 2025-11-09 09:05:22 +0700
categories: [journal]
tags: [handwritten, gallery, sketchbook]
description: "Testing a manga-style gallery layout for sharing handwritten notes."
image: /assets/images/handwritten-notes/page-000.webp
---

<style>
.handwritten-chapter {
  margin: 2rem 0;
  display: grid;
  gap: 1.5rem;
}

.handwritten-toolbar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.handwritten-toolbar button {
  border: none;
  background: #222;
  color: #f8f8f8;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.handwritten-toolbar button:focus-visible {
  outline: 3px solid #f6a821;
  outline-offset: 2px;
}

.handwritten-toolbar button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.18);
}

.handwritten-counter {
  font-weight: 600;
  font-size: 0.95rem;
  color: #555;
}

.handwritten-viewer {
  width: min(860px, 100%);
  margin: 0 auto;
  position: relative;
  background: #0f0f0f;
  border-radius: 18px;
  padding: clamp(1rem, 4vw, 1.5rem);
  box-shadow: 0 18px 35px rgba(15, 15, 15, 0.35);
}

.handwritten-viewer img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  background: #fff;
  display: block;
}

.handwritten-thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
}

.handwritten-thumb {
  border: none;
  background: transparent;
  padding: 8px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.2s ease;
  border: 2px solid transparent;
}

.handwritten-thumb.is-active {
  border-color: #f6a821;
  box-shadow: 0 0 0 4px rgba(246, 168, 33, 0.16);
}

.handwritten-thumb img {
  width: 100%;
  display: block;
  border-radius: 8px;
  background: #fff;
}

.handwritten-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.9rem;
}

.handwritten-actions a {
  color: #f6a821;
  text-decoration: none;
  font-weight: 600;
}

.handwritten-actions a:hover {
  text-decoration: underline;
}

@media (prefers-reduced-motion: reduce) {
  .handwritten-toolbar button,
  .handwritten-thumb {
    transition: none;
  }
}
</style>

<div class="handwritten-chapter" data-images='[
  "/assets/images/handwritten-notes/page-000.webp",
  "/assets/images/handwritten-notes/page-001.webp",
  "/assets/images/handwritten-notes/page-002.webp",
  "/assets/images/handwritten-notes/page-003.webp",
  "/assets/images/handwritten-notes/page-004.webp",
  "/assets/images/handwritten-notes/page-005.webp"
]'>
  <div class="handwritten-toolbar" role="group" aria-label="Gallery navigation">
    <button type="button" class="handwritten-nav" data-direction="prev" aria-label="Previous page">Prev</button>
    <span class="handwritten-counter"><span class="handwritten-current">1</span> / <span class="handwritten-total">6</span></span>
    <button type="button" class="handwritten-nav" data-direction="next" aria-label="Next page">Next</button>
  </div>

  <div class="handwritten-viewer">
    <img src="/assets/images/handwritten-notes/page-000.webp" alt="Handwritten notes page 1" loading="lazy">
  </div>

  <div class="handwritten-actions">
    <a href="/assets/images/handwritten-notes/page-000.webp" download target="_blank" rel="noopener">Download current page</a>
    <a href="/assets/images/handwritten-notes/page-000.webp" target="_blank" rel="noopener">Open in new tab</a>
  </div>

  <div class="handwritten-thumbs" aria-label="Page thumbnails">
    <button type="button" class="handwritten-thumb is-active" data-index="0">
      <img src="/assets/images/handwritten-notes/page-000.webp" alt="Page 1 thumbnail" loading="lazy">
    </button>
    <button type="button" class="handwritten-thumb" data-index="1">
      <img src="/assets/images/handwritten-notes/page-001.webp" alt="Page 2 thumbnail" loading="lazy">
    </button>
    <button type="button" class="handwritten-thumb" data-index="2">
      <img src="/assets/images/handwritten-notes/page-002.webp" alt="Page 3 thumbnail" loading="lazy">
    </button>
    <button type="button" class="handwritten-thumb" data-index="3">
      <img src="/assets/images/handwritten-notes/page-003.webp" alt="Page 4 thumbnail" loading="lazy">
    </button>
    <button type="button" class="handwritten-thumb" data-index="4">
      <img src="/assets/images/handwritten-notes/page-004.webp" alt="Page 5 thumbnail" loading="lazy">
    </button>
    <button type="button" class="handwritten-thumb" data-index="5">
      <img src="/assets/images/handwritten-notes/page-005.webp" alt="Page 6 thumbnail" loading="lazy">
    </button>
  </div>
</div>

<noscript>
  <p><strong>Heads up:</strong> Enable JavaScript to use the interactive gallery. Until then, here are the pages inline.</p>
  <div>
    <img src="/assets/images/handwritten-notes/page-000.webp" alt="Page 1 static view">
    <img src="/assets/images/handwritten-notes/page-001.webp" alt="Page 2 static view">
    <img src="/assets/images/handwritten-notes/page-002.webp" alt="Page 3 static view">
    <img src="/assets/images/handwritten-notes/page-003.webp" alt="Page 4 static view">
    <img src="/assets/images/handwritten-notes/page-004.webp" alt="Page 5 static view">
    <img src="/assets/images/handwritten-notes/page-005.webp" alt="Page 6 static view">
  </div>
</noscript>

<script>
(function () {
  const gallery = document.querySelector(".handwritten-chapter");
  if (!gallery) return;

  const dataImages = gallery.getAttribute("data-images");
  let images;
  try {
    images = JSON.parse(dataImages);
  } catch {
    images = Array.from(gallery.querySelectorAll(".handwritten-thumb img")).map(img => img.src);
  }

  const viewerImg = gallery.querySelector(".handwritten-viewer img");
  const counterCurrent = gallery.querySelector(".handwritten-current");
  const counterTotal = gallery.querySelector(".handwritten-total");
  const thumbs = Array.from(gallery.querySelectorAll(".handwritten-thumb"));
  const actionLinks = Array.from(gallery.querySelectorAll(".handwritten-actions a"));
  const total = images.length;

  counterTotal.textContent = total;
  let currentIndex = 0;

  const updateView = (nextIndex) => {
    const index = (nextIndex + total) % total;
    currentIndex = index;
    const src = images[index];
    viewerImg.src = src;
    viewerImg.alt = "Handwritten notes page " + (index + 1);
    counterCurrent.textContent = index + 1;

    actionLinks.forEach((link) => {
      const url = new URL(link.href, window.location.origin);
      url.pathname = src;
      link.href = url.toString();
    });

    thumbs.forEach((thumb, thumbIndex) => {
      thumb.classList.toggle("is-active", thumbIndex === index);
    });
  };

  gallery.querySelectorAll(".handwritten-nav").forEach((button) => {
    button.addEventListener("click", () => {
      const direction = button.getAttribute("data-direction") === "next" ? 1 : -1;
      updateView(currentIndex + direction);
    });
  });

  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      const index = Number(thumb.getAttribute("data-index"));
      updateView(index);
    });
  });

  document.addEventListener("keydown", (event) => {
    if (!gallery.contains(document.activeElement) && !window.getSelection().toString()) {
      if (event.key === "ArrowRight") {
        updateView(currentIndex + 1);
      } else if (event.key === "ArrowLeft") {
        updateView(currentIndex - 1);
      }
    }
  });
})();
</script>

