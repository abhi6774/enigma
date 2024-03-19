export async function fetchSessionData(sessionId) {
    const response = { data: null, error: null }
    try {
      const dataraw = await fetch(
        "http://localhost:8000/chat/s/" + sessionId,
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
      console.log(data)
      response.data = data;
    } catch (error) {
      console.log("Got error:", error);
      response.error = error;
    }
    return response;
  }
