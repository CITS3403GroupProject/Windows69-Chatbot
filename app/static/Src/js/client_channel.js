document.addEventListener("DOMContentLoaded", () => {
  // TODO: Use https in production

  // init variables
  let curr_channel_id = -1;
  let curr_user_id = parseInt(document.body.dataset.userId, 10);
  let curr_username = document.body.dataset.username;

  // socket init
  const socket = io.connect("http://" + document.domain + ":" + location.port);
  socket.emit("init", {});

  function createChannel(ch_init_data) {
    fetch("/api/v1/channels/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ch_init_data),
    })
      .then((response) => {
        // TODO: Create failure error
        if (!response.ok) {
          throw new Error("Failed to create channel.");
        }
        return response.json();
      })
      .then((data) => {
        console.log(`New channel created with ID: ${data.id}`);
      })
      .catch((error) => {
        // TODO: Create failure error
        console.error(error);
      });
  }

  function createBot(bot_init_data) {
    fetch("/api/v1/bots/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bot_init_data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to create Bot.");
        }
        return response.json();
      })
      .then((data) => {
        $("#bot_name")[0].value = ""
        $("#bot_begin_prompt")[0].value = ""
        $("#submit_bot").text("Bot Created!")
        
        
      })
      .catch(async (error) => {
        $("#bot_name")[0].value = ""
        $("#submit_bot").text("Bot creation failed... Try a new username.")
        await new Promise(r => setTimeout(r, 5000));
        $("#submit_bot").text("Submit")
        console.error(error);
      });
  }

  function setChangeChannelButtons(channels) {
    // clear channel list first.
    $("#channel_list").empty();
    console.log(channels);
    channels.forEach(function (channel) {
      let channel_id = channel[0];
      let channel_name = channel[1];
      // Create a new button element
      var item = $("<li></li>")
        .text(channel_name)
        .attr("data-channel-id", channel_id)
        .attr("data-channel-name", channel_name)
        .attr("class", "channel_button")
        .on("click", () => {
          changeChannel(channel_id);
        });
      $("#channel_list").append(item);
    });
  }

  function setInChannelList(users) {
    // clear user list first.
    $("#users_in_channel").empty();
    if (users == null) {
      return;
    }
    users.forEach(function (user) {
      let userID = user.id;
      let username = user.username;

      let userBtn = $("<button></button>")
        .text(username)
        .attr("class", "btn-user in-channel-user")
        .on("click", () => {});

      $("#users_in_channel").append(userBtn);
    });
  }

  function setNotInChannelList(users) {
    $("#users_not_in_channel").empty();
    if (users == null) {
      return;
    }
    users.forEach(function (user) {
      console.log(user);
      let userID = user.id;
      let username = user.username;

      let userBtn = $("<button></button>")
        .text(username)
        .attr("class", "btn-user not-in-channel-user")
        .on("click", () => {
          showAddUserBtn(userID, username);
        });

      $("#users_not_in_channel").append(userBtn);
    });
  }

  function showAddUserBtn(userID, username) {
    let addUserBtn = $("<button></button>")
      .text("Add User: " + username)
      .attr("class", "btn btn-wide")
      .on("click", () => {
        addUser([userID]);
      });
    $("#add_user_div").empty();
    $("#add_user_div").append(addUserBtn);
  }

  function setAddUsers() {
    if (curr_channel_id == -1) {
      setNotInChannelList(null);
      setInChannelList(null);
      return;
    }
    fetch(`/api/v1/channels/${curr_channel_id}/users`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        // TODO: Create failure error
        if (!response.ok) {
          throw new Error("Something went wrong.");
        }
        return response.json();
      })
      .then((users) => {
        setNotInChannelList(users.not_in_channel);
        setInChannelList(users.in_channel);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function changeChannel(channel_id) {
    history.length = 0;
    if (channel_id == null) {
      $("#history").empty()
      $("#channel_header").text("Join a channel to start talking!")
      curr_channel_id = -1;
    } else {
      $("#history").empty()
      $("#history").text("Loading...");
      socket.emit("change_channel", { channel_id: channel_id });
    }
  }

  function leaveChannel() {
    fetch(`/api/v1/channels/leave/${curr_channel_id}/${curr_user_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to leave channel.");
        }
        return response.json();
      })
      .then((data) => {
        // left current channel.
        changeChannel(null);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function getChannels() {
    fetch(`/api/v1/channels/user/${curr_user_id}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to get channels.");
        }
        return response.json();
      })
      .then((data) => {
        setChangeChannelButtons(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function addUser(data) {
    fetch(`/api/v1/channels/${curr_channel_id}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ users: data }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to add user.");
        }
        return response.json();
      })
      .then((data) => {
        // TODO: indicate success
        $("#add_user_div").empty();
      })
      .catch((error) => {
        // TODO: Create failure error
        console.error(error);
      });
  }

  socket.on("change_channel", (data) => {
    if (data == undefined) {
      curr_channel_id = -1;
      setAddUsers();
    } else if (!data.success) {
      alert("Unable to change channel.");
    } else {
      $("#channel_header")[0].innerText = "Welcome to:  " + data.channel_name;
      curr_channel_id = data.channel_id;
      setAddUsers();
      // $("#channel_header2")[0].innerText = "You are in channel: " + data.channel_name
    }
  });

  socket.on("user_channels", (data) => {
    setChangeChannelButtons(data);
  });

  socket.on("update_user_list", (data) => {
    setAddUsers();
  });

  // receiving history/new messages
  socket.on("history", (data) => {
    if(data.length > 0) {
      init = false
      if ($("#history").children().length === 0) {
        init = true
        $("#history").text("");
      }
      data.forEach((msg) => {
        let time = new Date(msg["timestamp"]);
        let sender = $('<span></span>').attr('class', "sender").text(msg["sender_name"]);
        let timestamp = $('<span></span>').attr('class', "timestamp").text(
          ` at ${time.getHours()}:${time.getMinutes()} on ${time.toLocaleDateString("en-GB")}: `
          );
        let content = $('<span></span>').attr('class', "msg_content").text(msg["text"]);

        let messageRow = $('<div></div>').append(sender).append(timestamp).append(content);
        messageRow.attr('class', "msg");
        $("#history").append(messageRow);
      });
    }
    if (init) {
      $("#history").scrollTop($("#history")[0].scrollHeight - 800);
    }
    if ($("#history").children().length === 0) {
      $("#history").text("No messages yet...");
    }
  });
  // send message
  $("#send_message")[0].onclick = () => {
    const text = $("#tx_data_field")[0].value;

    socket.emit("transmit_data", { text: text });
  };

  // changing channel
  $("#submit_channel")[0].onclick = () => {
    ch_data = {
      name: $("#channel_name")[0].value,
    };
    createChannel(ch_data);
  };

  $("#submit_bot")[0].onclick = async () => {
    bot_data = {
      name: $("#bot_name")[0].value,
      begin_prompt: $("#bot_begin_prompt")[0].value,
    }
    if(bot_data.name.includes(' ')) {
      $("#submit_bot").text("Do not include any spaces in the bot name.")
      await new Promise(r => setTimeout(r, 5000));
      $("#submit_bot").text("Submit")
    } else if (bot_data.name != "" && bot_data.begin_prompt != "") {
      $("#submit_bot").text("Creating bot.")
      await new Promise(r => setTimeout(r, 500));
      $("#submit_bot").text("Creating bot..")
      await new Promise(r => setTimeout(r, 500));
      $("#submit_bot").text("Creating bot...")
      await new Promise(r => setTimeout(r, 500));
      $("#submit_bot").text("Creating bot....")
      await new Promise(r => setTimeout(r, 500));
      $("#submit_bot").text("Creating bot.....")
      await new Promise(r => setTimeout(r, 500));
      createBot(bot_data);
    }
  };
  
  // add user to channel
  $("#leave_channel")[0].onclick = () => {
    leaveChannel();
  };

  function updateTime() {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();

    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;

    var time = hours + ":" + minutes;

    document.getElementById("time").innerHTML = time;
  }

  getChannels();

  // Update every second
  setInterval(updateTime, 1000);
});
