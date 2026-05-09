export const simulateSensorRequest = (path = "") => {
  const config = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // body: JSON.stringify({ device_name: id }),
  };

  return fetch("http://127.0.0.1:8050/api/simulate" + path, config)
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP error ${r.status}`);
      return r.json();
    })
    .catch((e) => console.error(e));
};

export const retriveData = (path, id) => {
  const config = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ device_name: id }),
  };

  return fetch("http://127.0.0.1:8050/api/device" + path, config)
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP error ${r.status}`);
      return r.json();
    })
    .catch((e) => console.error(e));
};


