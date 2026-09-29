/* Adapt Sphinx's named code blocks to Prism's Line Numbers / Line Highlight. */
(() => {
    function initializeExamples() {
        document.querySelectorAll(".code-example[id]").forEach((block) => {
            const pre = block.querySelector("pre");
            const language = Array.from(block.classList).find((name) => name.startsWith("highlight-"))?.slice(10);
            if (!pre || !Prism.languages[language]) return;

            // Keep ordinary Sphinx rendering when JavaScript is unavailable.
            pre.querySelectorAll(".linenos").forEach((number) => number.remove());
            const code = document.createElement("code");
            code.className = `language-${language}`;
            code.textContent = pre.textContent;
            pre.replaceChildren(code);
            pre.id = block.id;
            block.removeAttribute("id");
            pre.classList.add("line-numbers", "linkable-line-numbers");
            pre.dataset.line = "";
            pre.setAttribute("aria-label", `${language === "nix" ? "Nix" : "TOML"} code example`);
            Prism.highlightElement(code);
        });

        document.querySelectorAll("a.code-lines").forEach((link) => {
            const match = link.getAttribute("href")?.match(/^#(.+)\.(\d+(?:-\d+)?)$/);
            if (!match || !document.getElementById(match[1])?.classList.contains("linkable-line-numbers")) return;

            const range = match[2];
            const label = `Highlight ${range.includes("-") ? "lines" : "line"} ${range.replace("-", "–")}`;
            const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            icon.setAttribute("viewBox", "0 0 24 24");
            icon.setAttribute("aria-hidden", "true");
            icon.setAttribute("focusable", "false");
            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttribute("d", "m7 7-5 5 5 5m10-10 5 5-5 5m-3-14-4 18");
            icon.append(path);
            link.replaceChildren(icon);
            link.classList.add("code-lines-icon");
            link.setAttribute("aria-label", label);
            link.title = label;
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializeExamples, { once: true });
    } else {
        initializeExamples();
    }
})();
