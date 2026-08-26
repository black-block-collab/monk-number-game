from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

answer = random.randint(1, 100)
count = 0
low = 1
high = 100

html = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>お坊さんの数字当て修行</title>

<style>
body {
    margin: 0;
    min-height: 100vh;
    font-family: "Hiragino Sans", sans-serif;
    text-align: center;

    background-image:
        linear-gradient(rgba(255,255,255,0.15), rgba(255,255,255,0.15)),
        url("/static/monk_game_bg.png");

    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
}

.game {
    padding-top: 30px;
    padding-bottom: 60px;
}

h1 {
    font-size: 44px;
    color: #402713;
    text-shadow: 2px 2px 4px white;
}

.bubble {
    width: 500px;
    margin: 280px auto 20px auto;
    background: rgba(255,255,255,0.95);
    border: 4px solid #49301d;
    border-radius: 30px;
    padding: 20px;
    font-size: 27px;
    font-weight: bold;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

.info {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px;
}

.card {
    background: rgba(255,248,220,0.95);
    border: 2px solid #72522f;
    border-radius: 15px;
    padding: 12px 25px;
    font-size: 20px;
}

input {
    width: 180px;
    font-size: 30px;
    text-align: center;
    padding: 14px;
    border-radius: 15px;
    border: 3px solid #79552e;
}

button {
    font-size: 22px;
    padding: 15px 30px;
    margin: 8px;
    border: none;
    border-radius: 15px;
    cursor: pointer;
}

.answer {
    background: #317a43;
    color: white;
}

.restart {
    background: #c88a35;
    color: white;
}

.sound {
    background: #4b6d89;
    color: white;
}
</style>
</head>

<body>

<div class="game">

<h1>お坊さんの数字当て修行</h1>

<div class="bubble" id="message">
    {{ message }}
</div>

<div class="info">

    <div class="card">
        挑戦回数<br>
        <strong>{{ count }}回</strong>
    </div>

    <div class="card">
        現在の範囲<br>
        <strong>{{ low }} ～ {{ high }}</strong>
    </div>

</div>

<form method="POST">

    <input
        type="number"
        name="guess"
        min="1"
        max="100"
        placeholder="1～100"
        required
        autofocus
    >

    <br>

    <button class="answer" type="submit">
        答える
    </button>

</form>

<form method="POST">

    <input type="hidden" name="restart" value="yes">

    <button class="restart" type="submit">
        もう一度修行する
    </button>

</form>

<button class="sound" onclick="speakMessage()">
    🔊 お坊さんに喋ってもらう
</button>

</div>

<script>

function speakMessage() {

    const text =
        document.getElementById("message").innerText;

    speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "ja-JP";
    speech.rate = 0.85;
    speech.pitch = 0.8;

    speechSynthesis.speak(speech);
}

// 数字を答えた後は自動で喋る
{% if speak %}
window.onload = function() {
    setTimeout(speakMessage, 300);
};
{% endif %}

</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def game():

    global answer, count, low, high

    message = "1から100までの数字を申してみよ"
    speak = False

    if request.method == "POST":

        # 最初からやり直す
        if request.form.get("restart") == "yes":

            answer = random.randint(1, 100)
            count = 0
            low = 1
            high = 100

            message = "新しい修行じゃ。数字を申してみよ"
            speak = True

        else:

            guess = int(request.form["guess"])
            count += 1
            speak = True

            if guess < answer:

                message = "もっと大きい数字じゃ！"

                if guess >= low:
                    low = guess + 1

            elif guess > answer:

                message = "もっと小さい数字じゃ！"

                if guess <= high:
                    high = guess - 1

            else:

                message = (
                    f"見事じゃ！ "
                    f"{answer} が正解じゃ！ "
                    f"{count}回で修行達成じゃ！"
                )

    return render_template_string(
        html,
        message=message,
        count=count,
        low=low,
        high=high,
        speak=speak
    )


if __name__ == "__main__":
    app.run(debug=True)