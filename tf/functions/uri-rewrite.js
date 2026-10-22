function handler(event) {
  const request = event.request;
  const uri = request.uri;
  if (uri.endsWith('/')) {
    request.uri = uri + 'index.html';
  } else if (!uri.slice(uri.lastIndexOf('/')).includes('.')) {
    request.uri = uri + '.html';
  }
  return request;
}
