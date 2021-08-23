% rebase('site/base.tpl')
% import model

<section>
  <div class="front_page">
    <h1 class="headline">Four in a row</h1>
    <form action="/new_game/{{model.PLYR}}/{{model.HARD}}" method="post">
      <button class="button_fp_plyr" type="submit">Hard - Player starts</button>
    </form>
    <form action="/new_game/{{model.PLYR}}/{{model.EASY}}" method="post">
      <button class="button_fp_plyr" type="submit">Easy - Player starts</button>
    </form>
    <form action="/new_game/{{model.CMPTR}}/{{model.HARD}}" method="post">
      <button class="button_fp_cmptr" type="submit">Hard - Computer starts</button>
    </form>
    <form action="/new_game/{{model.CMPTR}}/{{model.EASY}}" method="post">
      <button class="button_fp_cmptr" type="submit">Easy - Computer starts</button>
    </form>
    <form action="/new_game/{{model.PLYRS_1}}/{{model.HARD}}" method="post">
      <button class="button_fp_plyr" type="submit">Two players</button>
    </form>
  </div>
</section>

<section>
  <div id="s1">
      <img src="/static/Player.png" class="picture"/>
  </div>
  <div id="s2">
      <h1 class="name">You</h1>
  </div>
  <div id="s3">
      <h1 class="name">Com</h1>
  </div>
  <div id="s4">
      <img src="/static/Computer.png" class="picture"/>
  </div>
</section>
