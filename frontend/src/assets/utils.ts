const send = async (method: string, url: string, data: any = null) => {
  const server_url = `/api/${url}`;
  try {
    const response = await fetch(server_url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      ...(data ? { body: JSON.stringify(data) } : {}),
    });

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText}`);
      return {};
    }

    const json = await response.json();
    return json;
  } catch (err) {
    console.error("Network or parsing error:", err);
    return {};
  }
};

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

function isEmpty(obj: any) {
  for (const prop in obj) {
    if (Object.hasOwn(obj, prop)) {
      return false;
    }
  }

  return true;
}

export { send, sleep, isEmpty };
