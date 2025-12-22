import axios from "axios";
const API_URL = "https://my-sudoku-api.onrender.com";
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

const handleRequest = async requestPromise => {
  try {
    const response = await requestPromise;
    return [response.data, null];
  } catch (error) {
    console.error("API Error:", error.response || error.message);
    return [null, error.response?.data || { message: error.message }];
  }
};

export const generateNewGame = difficulty => {
  return handleRequest(
    apiClient.post("/api/generate", { difficulty: difficulty })
  );
};

export const solveBoard = board => {
  return handleRequest(apiClient.post("/api/solve", { board: board }));
};

export const saveGame = (game_id, board, name) => {
  return handleRequest(
    apiClient.post("/api/save", {
      game_id: game_id,
      current_board: board,
      name: name,
    })
  );
};

export const loadGameByName = name => {
  const encodedName = encodeURIComponent(name);
  return handleRequest(apiClient.get(`/api/load_by_name/${encodedName}`));
};

export const finishGame = (game_id, final_board) => {
  return handleRequest(
    apiClient.post("/api/finish", {
      game_id: game_id,
      final_board: final_board,
    })
  );
};

export const getHtmlReportUrl = () => {
  return `${apiClient.defaults.baseURL}/api/report/html`;
};

export const getPdfReportUrl = () => {
  return `${apiClient.defaults.baseURL}/api/report/pdf`;
};

export const getSavedGamesList = () => {
  return handleRequest(apiClient.get("/api/saves"));
};

export const deleteGameByName = name => {
  const encodedName = encodeURIComponent(name);
  return handleRequest(apiClient.delete(`/api/delete/${encodedName}`));
};

export const startCustomGame = board => {
  return handleRequest(apiClient.post("/api/start_custom_game", { board }));
};
