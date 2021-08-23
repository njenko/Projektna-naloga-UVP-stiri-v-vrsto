% rebase('site/base.tpl')
% import model

<section>
  <div class="top">
    <table class="buttons">
      % if game.player == model.PLYRS_1 or game.player == model.PLYRS_2:
        % if move == model.PLYR:
          <tr><td id="winner"><h1 class="desc">Player one won!</h1></td></tr>
        % elif move == model.CMPTR:
          <tr><td id="loser"><h1 class="desc">Player two won!</h1></td></tr>
        % elif move == model.DRAW:
          <td class="draw">
            <h1>Draw!</h1>
          </td>
        % else:
          <tr>
            % if game.player == model.PLYRS_1:
              % for i in range(model.COLLUMNS):
                <td>
                  <form action="/make_a_move/{{i}}" method="post">
                    <button class="button" type="submit">{{i + 1}}</button>
                  </form>
                </td>
              % end
            % else:
              % for i in range(model.COLLUMNS):
                <td>
                  <form action="/make_a_move/{{i}}" method="post">
                    <button class="button1" type="submit">{{i + 1}}</button>
                  </form>
                </td>
              % end
            % end
          </tr>
        % end        
      % else:
        % if move == model.PLYR:
          <tr><td id="winner"><h1 class="desc">You won!</h1></td></tr>
        % elif move == model.CMPTR:
          <tr><td id="loser"><h1 class="desc">You lost!</h1></td></tr>
        % elif move == model.DRAW:
          <td class="draw">
            <h1>Draw!</h1>
          </td>
        % else:
          <tr>
            % for i in range(model.COLLUMNS):
              <td>
                <form action="/make_a_move/{{i}}" method="post">
                  <button class="button" type="submit">{{i + 1}}</button>
                </form>
              </td>
            % end
          </tr>
        % end
      % end
    </table>
  </div>


  <div>
    <table class="board">
      % for row in range(model.ROWS):
        <tr valign="middel">
          % for collumn in range(model.COLLUMNS):
          <td>
            % if game.board[row][collumn] == model.EMPTY:
              <img src="/static/White.jpg" width="100%"  /> 
            % elif game.board[row][collumn] == model.CMPTR:
              <img src="/static/Yellow.jpg" width="100%"  />
            % else:
              <img src="/static/Red.jpg" width="100%"  />
            % end
          </td>
          % end
        </tr>
      % end
    </table>
  </div>

  <div>
    <table class="reset">
      <tr>
        % if move == model.PLYR or move == model.CMPTR or move == model.DRAW:
          <td>
            <form action="/" method="post">
              <button class="button" type="submit">New game</button>
            </form>
          </td>
        % elif move == model.ERR:
        <td class="error">         
          <h1>Incorrect move!!!</h1>
        </td>
        % else:
          <td>
            <form action="/" method="post">
              <button class="button" type="submit">Reset</button>
            </form>
          </td>
        % end
      </tr>
    </table>
  </div>
</section>

<section>
  <div id="s1">
    <img src="/static/Player.png" class="picture"/>
  </div>
  <div id="s2">
    % if game.player == model.PLYRS_1 or game.player == model.PLYRS_2:
      <h1 class="name">Player one</h1>
    % else:
      <h1 class="name">You</h1>
    % end
  </div>
  <div id="s3">
    % if game.player == model.PLYRS_1 or game.player == model.PLYRS_2:
      <h1 class="name">Player two</h1>
    % else:
      <h1 class="name">Com</h1>
    % end
  </div>
  <div id="s4">
      <img src="/static/Computer.png" class="picture"/>
  </div>
</section>

