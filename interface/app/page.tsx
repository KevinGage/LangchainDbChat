"use client";
import { useState } from "react";
import axios from "axios";
import LoadingSpinner from "./spinner";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState({
    question: "",
    answer: "",
    code_llm_answer: "",
    query: "",
    sql_data: "",
  });
  const [showDetails, setShowDetails] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleQuestionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAnswer({
      question: "",
      answer: "",
      code_llm_answer: "",
      query: "",
      sql_data: "",
    });
    setLoading(true);
    const response = await axios.post("http://127.0.0.1:8000/question", {
      question,
    });
    setAnswer(response.data);
    setLoading(false);
  };

  const toggleDetails = (e: React.FormEvent) => {
    e.preventDefault();
    setShowDetails(!showDetails);
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-10">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center w-3/4"
      >
        <input
          type="text"
          value={question}
          onChange={handleQuestionChange}
          className="border border-gray-300 rounded-md px-4 py-2 mb-4  w-full"
          placeholder="Enter your question"
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md mb-4"
        >
          Submit Question
        </button>
      </form>
      {loading ? <LoadingSpinner /> : null}
      {answer.answer ? (
        <div className="flex flex-col items-center w-3/4">
          <div className="flex flex-col items-center w-full">
            <textarea
              value={answer.answer}
              readOnly
              className="border border-gray-300 rounded-md px-4 py-2 mb-4 w-full"
              placeholder="Answer will appear here"
            />
          </div>

          <div className="flex flex-col items-center w-full">
            <button
              onClick={toggleDetails}
              className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-md mb-4"
            >
              Toggle Response Details
            </button>
            {showDetails && (
              <div className="flex flex-col items-center w-full">
                <h2>Code LLM Answer</h2>
                <textarea
                  value={answer.code_llm_answer}
                  readOnly
                  className="border border-gray-300 rounded-md px-4 py-2 mb-4 w-full"
                />
                <h2>SQL Query</h2>
                <textarea
                  value={answer.query}
                  readOnly
                  className="border border-gray-300 rounded-md px-4 py-2 mb-4 w-full"
                />
                <h2>SQL Query Result</h2>
                <textarea
                  value={answer.sql_data}
                  readOnly
                  className="border border-gray-300 rounded-md px-4 py-2 mb-4 w-full"
                />
              </div>
            )}
          </div>
        </div>
      ) : null}
    </main>
  );
}
