<!DOCTYPE html>
<html lang="en">
  

  <head>
    <title>Štiri v vrsto</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Nejc Jenko">
  </head>


  <style>
    body{
      width: 40%;
      margin: auto;
      background-image: url("/static/Background.jpg");
    }
    .front_page{
      margin-bottom: 1vw;
    }
    .top{
      margin-top: 4vw;
    }
    .buttons{
      border-spacing: 0;
      width: 100%;
    }
    .buttons td{
      line-height: 0;
      padding: 0;
    }
    .button, .button1{
      width: 100%;
      height: 2vw;
      font-size: 1vw;
      border: 0;
      background: #24305e;
      font-family: Arial, Helvetica, sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      color: #c1d9e6;
    }
    .button:hover{
      outline: none;
      background: #f76c6c;
      color: #24305e;
    }
    .button1:hover{
      outline: none;
      background: #f8e9a1;
      color: #24305e;
    }
    .button:active, .button1:active{
      outline: none;
    }
    .board{
      border-spacing: 0;
    }
    .board td{
      line-height: 0;
      padding: 0;
    }
    .reset{
      border-spacing: 0;
      width: 100%;
    }
    .reset td{
      line-height: 0;
      padding: 0;
    }
    #winner{
      height: 2vw;
      font-size: 1vw;
      background: #f76c6c;
      text-align: center;
    }
    #loser{
      height: 2vw;
      font-size: 1vw;
      background: #f8e9a1;
      text-align: center;
    }
    .draw{
      height: 2vw;
      font-size: 1vw;
      background: #24305e;
      text-align: center;
    }
    .draw h1{
      font-family: Arial, Helvetica, sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      color: #c1d9e6;
      font-size: 1vw;
    }
    .desc{
      font-family: Arial, Helvetica, sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      color: #24305e;
      font-size: 1vw;
    }
    .error{
      width: 100%;
      height: 2vw;
      background: #24305e;
      text-align: center;
      font-size: 1vw;
      font-family: Arial, Helvetica, sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      color: #c1d9e6;
      margin: auto;
    }
    #s1{
      float: left;
      width: 15%;
    }
    #s2{
      float: left;
      width: 60%;
    }
    #s3{
      float: right;
      width: 10%;
    }
    #s4{
      float: right;
      width: 15%;
    }
    .picture{
      width: 80%;
    }
    .name{
      font-family: Arial, Helvetica, sans-serif;
      font-size: 1.3vw;
      color: #24305e;
      font-weight: bold;
      text-transform: uppercase;
      margin-top: 2vw;
    }
    .headline{
      font-family: Arial, Helvetica, sans-serif;
      font-size: 3.5vw;
      color: #24305e;
      font-weight: 900;
      text-transform: uppercase;
      margin-top:  15vw;
      margin-bottom: 4vw;
      text-align: center;
    }
    .button_fp_cmptr, .button_fp_plyr{
      width: 100%;
      height: 3vw;
      font-size: 2vw;
      border: 0;
      background: #24305e;
      font-family: Arial, Helvetica, sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      color: #c1d9e6;
      margin-bottom: 0.5vw;
    }
    .button_fp_plyr:hover{
      outline: none;
      background: #f76c6c;
      color: #24305e;
    }
    .button_fp_plyr:active{
      outline: none;
    }
    .button_fp_cmptr:hover{
      outline: none;
      background: #f8e9a1;
      color: #24305e;
    }
    .button_fp_cmptr:active{
      outline: none;
    }
  </style>


  <body >
    {{!base}}
  </body>


</html>
