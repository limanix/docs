// Resolve directory indexes while preserving Sphinx .html pages and static assets.
function handler(event) {
  const request = event.request;

  if (request.uri.endsWith('/')) {
    request.uri += 'index.html';
  }

  return request;
}
