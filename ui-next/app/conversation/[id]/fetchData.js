export async function fetchSessionData(sessionId) {
    const response = { data: null, error: null }
    try {
      const dataraw = await fetch(
        "http://192.168.200.169:8000/chat/s/" + sessionId,
        {
          method: "GET",
        }
      );

      if (!dataraw.ok) {
        console.log("API not working");
        return;
      }

      /**
       * @type {SessionFetchAPIResponse}
       */
      const data = await dataraw.json();
      response.data = data;
    } catch (error) {
      console.log("Got error:", error);
      response.error = error;
    }
    return response;
  }
