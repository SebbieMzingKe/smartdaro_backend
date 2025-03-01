const {
    GoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
  } = require("@google/generative-ai");
  const { GoogleAIFileManager } = require("@google/generative-ai/server");
  
  const apiKey = process.env.GEMINI_API_KEY;
  const genAI = new GoogleGenerativeAI(apiKey);
  const fileManager = new GoogleAIFileManager(apiKey);
  
  /**
   * Uploads the given file to Gemini.
   *
   * See https://ai.google.dev/gemini-api/docs/prompting_with_media
   */
  async function uploadToGemini(path, mimeType) {
    const uploadResult = await fileManager.uploadFile(path, {
      mimeType,
      displayName: path,
    });
    const file = uploadResult.file;
    console.log(`Uploaded file ${file.displayName} as: ${file.name}`);
    return file;
  }
  
  const model = genAI.getGenerativeModel({
    model: "gemini-2.0-flash",
    systemInstruction: "\"I am building an AI-powered university timetable scheduling system using Django Rest Framework as the backend. The goal is to prevent venue clashes and optimize lecturer and student schedules automatically.\n\nThe AI should:\n\nTake input data on:\nCourses offered\nAvailable rooms with capacity\nLecturers (full-time or part-time)\nPreferred teaching times and constraints\nNumber of students per course\nGenerate an optimized timetable that ensures:\nNo room has overlapping classes\nLecturers are not assigned to multiple classes at the same time\nPart-time lecturers get suitable time slots\nEfficient use of available resources (rooms, time slots)\nProvide an API endpoint that allows the Django backend to request and store generated timetables.\nImplementation Requirements:\nThe AI model should use constraint-based optimization (e.g., Google OR-Tools, Genetic Algorithm, or Linear Programming).\nThe system should return a JSON response with properly assigned courses, rooms, and lecturer schedules.\nThe algorithm should prioritize fairness, ensuring an even distribution of workload across lecturers.\nCan you generate the AI model code in Python that will handle this scheduling logic and return the structured timetable as JSON?\"\n\n",
  });
  
  const generationConfig = {
    temperature: 1,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 8192,
    responseMimeType: "text/plain",
  };
  
  async function run() {
    // TODO Make these files available on the local file system
    // You may need to update the file paths
    const files = [
      await uploadToGemini("Unknown File", "application/octet-stream"),
    ];
  
    const chatSession = model.startChat({
      generationConfig,
      history: [
        {
          role: "user",
          parts: [
            {text: "{\n  \"rooms\": [\n    { \"room_name\": \"Room 101\", \"capacity\": 50, \"type\": \"Lecture Hall\", \"location\": \"Block A\" },\n    { \"room_name\": \"Room 102\", \"capacity\": 40, \"type\": \"Lecture Hall\", \"location\": \"Block A\" },\n    { \"room_name\": \"Lab 201\", \"capacity\": 30, \"type\": \"Computer Lab\", \"location\": \"Block B\" },\n    { \"room_name\": \"Hall 1\", \"capacity\": 200, \"type\": \"Auditorium\", \"location\": \"Block C\" },\n    { \"room_name\": \"Seminar 303\", \"capacity\": 20, \"type\": \"Seminar Room\", \"location\": \"Block D\" }\n  ],\n  \n  \"lecturers\": [\n    { \"name\": \"Dr. Kimani\", \"type\": \"Full-time\", \"max_hours_per_week\": 12, \"preferred_days\": [\"Monday\", \"Wednesday\", \"Friday\"], \"courses\": [\"AI 201\", \"Data Science\"] },\n    { \"name\": \"Prof. Atieno\", \"type\": \"Part-time\", \"max_hours_per_week\": 6, \"preferred_days\": [\"Tuesday\", \"Thursday\"], \"courses\": [\"CYB 301\"] },\n    { \"name\": \"Mr. Omondi\", \"type\": \"Full-time\", \"max_hours_per_week\": 15, \"preferred_days\": [\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\"], \"courses\": [\"CSC 101\", \"Web Development\", \"Python\"] },\n    { \"name\": \"Dr. Njeri\", \"type\": \"Full-time\", \"max_hours_per_week\": 10, \"preferred_days\": [\"Monday\", \"Wednesday\"], \"courses\": [\"ML 401\"] },\n    { \"name\": \"Mr. Kiptoo\", \"type\": \"Part-time\", \"max_hours_per_week\": 8, \"preferred_days\": [\"Tuesday\", \"Thursday\"], \"courses\": [\"SWE 202\"] }\n  ],\n\n  \"courses\": [\n    { \"course_code\": \"CSC 101\", \"course_name\": \"Introduction to CS\", \"lecturer\": \"Mr. Omondi\", \"students\": 100, \"preferred_venue\": \"Lecture Hall\", \"duration\": 3 },\n    { \"course_code\": \"AI 201\", \"course_name\": \"Artificial Intelligence\", \"lecturer\": \"Dr. Kimani\", \"students\": 50, \"preferred_venue\": \"Computer Lab\", \"duration\": 3 },\n    { \"course_code\": \"CYB 301\", \"course_name\": \"Cybersecurity Basics\", \"lecturer\": \"Prof. Atieno\", \"students\": 30, \"preferred_venue\": \"Seminar Room\", \"duration\": 3 },\n    { \"course_code\": \"ML 401\", \"course_name\": \"Machine Learning\", \"lecturer\": \"Dr. Njeri\", \"students\": 40, \"preferred_venue\": \"Lecture Hall\", \"duration\": 3 },\n    { \"course_code\": \"SWE 202\", \"course_name\": \"Software Engineering\", \"lecturer\": \"Mr. Kiptoo\", \"students\": 60, \"preferred_venue\": \"Lecture Hall\", \"duration\": 3 }\n  ],\n\n  \"time_slots\": {\n    \"Monday\": [\"08:00-11:00\", \"11:00-14:00\", \"14:00-17:00\"],\n    \"Tuesday\": [\"08:00-11:00\", \"11:00-14:00\", \"14:00-17:00\"],\n    \"Wednesday\": [\"08:00-11:00\", \"11:00-14:00\", \"14:00-17:00\"],\n    \"Thursday\": [\"08:00-11:00\", \"11:00-14:00\", \"14:00-17:00\"],\n    \"Friday\": [\"08:00-11:00\", \"11:00-14:00\", \"14:00-17:00\"]\n  }\n}\n"},
          ],
        },
        {
          role: "model",
          parts: [
            {
              fileData: {
                mimeType: files[0].mimeType,
                fileUri: files[0].uri,
              },
            },
          ],
        },
      ],
    });
  
    const result = await chatSession.sendMessage("INSERT_INPUT_HERE");
    console.log(result.response.text());
  }
  
  run();


  GEMINI_API_KEY=AIzaSyAOujVQ2SJvvgwjIKOocLVQJRu_N0p7YnY