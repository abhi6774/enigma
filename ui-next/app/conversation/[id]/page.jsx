"use client";
import styles from "./convostyles.module.scss";
import Navbar from "../../components/navbar";
import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import React from "react";
import { fetchSessionData } from "./fetchData";

function Convo({ params }) {

  const session_id = params.id;
  const [sessionData, setSessionData] = useState(null);

  const [inputQuery, setInputQuery] = useState("");
  const [chatData, setChatData] = useState([]);

  useEffect(() => {
    fetchSessionData(session_id)
    .then(({data, error}) => {
      if (error) {
        setSessionData(null);
      } else
      setSessionData(data);
    })
  }, []);
  
  useEffect(() => {
    if (sessionData)
      setChatData(sessionData.messages)
  }, [sessionData])

  async function handleSubmit() {
    if (inputQuery.trim() === "") return;

    const dataTemplate = {
      id: chatData.length + 1,
      question: inputQuery,
      answer: "",
    };

    setChatData((prevChatData) => [...prevChatData, dataTemplate]);
    document.querySelector("#query").value = "";

    scrollToBottom();

    apifetch(inputQuery);
  }

  const mainElement = document.querySelector("#\\#main");

  function scrollToBottom() {
    mainElement.scrollTop = mainElement.scrollHeight;
    const el = document.querySelector("#c_con")
    el.scrollBy(0, el.scrollHeight)
  }

  const handleKeyPressOnInput = (e) => {
    if (e.key === "Enter" && inputQuery.trim() !== "") {
      e.preventDefault();
      handleSubmit();
    }
  };

  async function apifetch(query) {
    try {
      const dataraw = await fetch(
        "http://localhost:8000/chat/" + sessionData._session_id,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            content: query,
          }),
        }
      );

      if (!dataraw.ok) {
        console.log("API not working");
        return;
      }

      const data = await dataraw.json();
      console.log(data);

      setChatData((prevChatData) => {
        const updatedChatData = [...prevChatData];
        updatedChatData[updatedChatData.length - 1].answer = data;
        console.log(chatData);
        return updatedChatData;
      });

      scrollToBottom();
      console.log(document.querySelector("#\\#main").scrollHeight);
    } catch (error) {
      console.log("Got error:", error);
    }
  }

  if (!sessionData) {
    return <div>Loading...</div>
  }

  return (
    <div className={styles.parentContainer}>
      <Navbar />

      <div id="#main" className={styles.main}>
        <div id="c_con" style={{ overflow: "scroll", width: "100vw", height: "calc(100vh - 4.5rem)", scrollBehavior: "smooth" }}>
          <div id={styles.containers}>
            <h2>
              <img
                className={styles.robotIconImg}
                src="/img/robotIcoEdit.png"
                alt="roboIcon"
              />
              Summary-
            </h2>
            <p className={styles.summary}>{sessionData.summary}</p>
            <h2 className={styles.secondhead}>Key Entities-</h2>
            <ul className={styles.keypoints}>
              {sessionData.key_entities.map((input, index) => {
                return <li key={index}>{input}</li>;
              })}
            </ul>
          </div>
          {chatData.map((input, index) => {
            return (
              <React.Fragment key={index}>
                <div id={styles.containers}>
                  <h2 className={styles.marginTop1rem}>
                    <img
                      className={styles.youLogo}
                      src="/img/youLogo.png"
                      alt="user logo"
                    />
                    You
                  </h2>
                  <p key={input.id} className={styles.que}>
                    {" "}
                    {input.question}{" "}
                  </p>
                </div>
                <div id={styles.containers}>
                  <h2>
                    <img
                      className={styles.robotIconImg}
                      src="/img/robotIcoEdit.png"
                      alt="roboIcon"
                    />
                    Enigma
                  </h2>
                  <p key={input.id} className={styles.ans}>
                    {" "}
                    {input.answer}{" "}
                  </p>
                </div>
              </React.Fragment>
            );
          })}
        </div>

        <div>
          <div className={styles.inputbox}>
            <form action="" method="post">
              <textarea
                onChange={(e) => setInputQuery(e.target.value)}
                onKeyDown={(e) => handleKeyPressOnInput(e)}
                type="text"
                name="query"
                id="query"
                autoFocus={true}
                placeholder="Ask more on it"
              ></textarea>
              <div
                onClick={(e) => handleSubmit(e)}
                className={styles.imageContainer}
              >
                <Image
                  className={styles.inputArrow}
                  src="/img/inputArrow.png"
                  width={22}
                  height={15}
                  alt="input arrow"
                />
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
  
}
export default Convo;
