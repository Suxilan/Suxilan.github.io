// Clean blockquote math lines starting with '>' and re-render KaTeX if available
(function () {
  function walk(node, callback) {
    if (node.nodeType === Node.TEXT_NODE) {
      callback(node);
      return;
    }
    if (!node.childNodes) return;
    for (var i = 0; i < node.childNodes.length; i++) {
      walk(node.childNodes[i], callback);
    }
  }

  function hasDoublePair(text) {
    return (text.match(/\$\$/g) || []).length >= 2;
  }

  function cleanBlockquoteMath(blockquote) {
    var changed = false;
    var displayMath = false;
    var envDepth = 0;

    walk(blockquote, function (textNode) {
      var value = textNode.nodeValue;
      if (!value || value.indexOf('>') === -1) return;

      var parts = value.split(/(\r?\n)/);
      var nextValue = '';

      for (var i = 0; i < parts.length; i++) {
        var part = parts[i];
        if (part === '\\n' || part === '\\r' || part === '\\r\n' || part.match(/^\r?\n$/)) {
          nextValue += part;
          continue;
        }

        var match = part.match(/^(\s*)(?:>\s*|&gt;\s*)(.*)$/);
        if (!match) {
          nextValue += part;
          continue;
        }

        var prefix = match[1] || '';
        var content = match[2];
        var trimmed = content.trimStart();
        var singleLineDollar = false;
        var shouldStrip = false;

        if (trimmed.startsWith('')) {
          if (hasDoublePair(trimmed) && trimmed.length > 2) {
            singleLineDollar = true;
          } else {
            if (!displayMath && envDepth === 0) {
              displayMath = true;
            } else {
              displayMath = false;
            }
          }
          shouldStrip = true;
        } else if (trimmed.startsWith('\\[')) {
          displayMath = true;
          shouldStrip = true;
        } else if (trimmed.startsWith('\\]')) {
          displayMath = false;
          shouldStrip = true;
        } else if (trimmed.startsWith('\\begin')) {
          envDepth++;
          shouldStrip = true;
        } else if (trimmed.startsWith('\\end')) {
          if (envDepth > 0) envDepth--;
          shouldStrip = true;
        } else if (displayMath || envDepth > 0) {
          shouldStrip = true;
        }

        if (shouldStrip) {
          nextValue += prefix + content;
          changed = true;
        } else {
          nextValue += part;
        }

        if (singleLineDollar) {
          // no state change for $...$ on single line
        }
      }

      if (changed) {
        textNode.nodeValue = nextValue;
      }
    });

    return changed;
  }

  function reRenderMath(root) {
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(root || document.body, {
          delimiters: [
            { left: '', right: '', display: true },
            { left: '\\[', right: '\\]', display: true },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false
        });
      } catch (e) { /* ignore */ }
    }
  }

  function processBlockquotes() {
    document.querySelectorAll('blockquote').forEach(function (bq) {
      var changed = cleanBlockquoteMath(bq);
      if (changed) {
        reRenderMath(bq);
      }
    });
  }

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    processBlockquotes();
  } else {
    document.addEventListener('DOMContentLoaded', processBlockquotes);
  }
})();

