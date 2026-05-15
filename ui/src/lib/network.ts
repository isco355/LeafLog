// const HOSTNAME = "http://127.0.0.1:8050/api"
const HOSTNAME = "http://0.0.0.0:8050/api"
// const HOSTNAME = "http://10.38.0.186:8050/api"
export const getDevices = () => {
  const url = HOSTNAME + "/devices/latest";
  return fetch(url).then((r) => {
    if (!r.ok) throw new Error(`HTTP error ${r.status}`);
    return r.json();
  }).catch((e) => console.error(e));
}
export const simulateSensorRequest = (path = "") => {
  const config = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  };

  return fetch(HOSTNAME + "/simulate" + path, config)
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

  return fetch(HOSTNAME + "/device" + path, config)
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP error ${r.status}`);
      return r.json();
    })
    .catch((e) => console.error(e));
};


