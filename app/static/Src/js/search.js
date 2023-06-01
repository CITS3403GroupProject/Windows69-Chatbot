MIN_SEARCH_TEXT_LEN = 2;

$(document).ready(() => {
  $("#search-query").on("input", () => {
    const searchQuery = $("#search-query").val();
    const searchResultsDiv = $("#search_results");
    if (searchQuery.trim() === "") {
      searchResultsDiv.html("<p>Please enter a search query.</p>");
    } else if (searchQuery.trim().length < MIN_SEARCH_TEXT_LEN) {
      searchResultsDiv.html(
        "<p>Enter longer search query (min length " +
          MIN_SEARCH_TEXT_LEN +
          ").</p>"
      );
    } else {
      searchMessages(searchQuery);
    }
  });

  const searchMessages = (searchQuery) => {
    const url = `/api/v1/messages/search`;
    const requestData = {
      search_query: searchQuery,
    };

    $.ajax({
      url: url,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(requestData),
      success: (data) => {
        displaySearchResults(data);
      },
      error: () => {
        console.log("An error occurred during the search.");
        alert("An error occurred during the search.");
      },
    });
  };
  const displaySearchResults = (data) => {
    const searchResultsDiv = $("#search_results");
    searchResultsDiv.empty();
    if (data.length === 0) {
      searchResultsDiv.html("<p>No search results found.</p>");
    } else {
      data.forEach((message) => {
        console.log(message)
        const messagesList = $("<div>").addClass("messages-list");
          const messageContainer = $("<div>").addClass("message-container");
          const senderName = $("<span>")
            .addClass("sender")
            .text("Sender: " + message.message_sender + " at ")
          const timestamp = $("<span>")
            .addClass("timestamp")
            .text(formatTimestamp(message.timestamp) + "\n");
          const messageText = $("<span>")
            .addClass("msg_content")
            .text(message.text);

          messageContainer.append(senderName, timestamp, messageText);
          messagesList.append(messageContainer);
        searchResultsDiv.append(messagesList);
      });
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.getHours() + ":" + date.getMinutes() + ", " + date.toLocaleDateString("en-GB");
  };
});
