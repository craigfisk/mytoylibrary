const query = `[out:json];
node["amenity"="community_centre"](44.7,-93.5,45.2,-92.9);
out 20;`
fetch('https://overpass-api.de/api/interpreter', {
  method: 'POST',
  body: query
}).then(res => res.text()).then(console.log).catch(console.error);
