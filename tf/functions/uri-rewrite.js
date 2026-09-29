function handler(event) {
  const request = event.request;

  if (request.uri === '/client/' || request.uri === '/client/index.html') {
    return {
      statusCode: 302,
      statusDescription: 'Found',
      headers: { location: { value: '/' } },
    };
  }
  if (request.uri.endsWith('/')) {
    request.uri += 'index.html';
  }
  return request;
}
