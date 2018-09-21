
var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console()), {
    colorize: true
};
logger.level = 'debug';
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ');
    logger.info(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    // Listen for messages that start with `!`
    if (message.substring(0, 1) == '!') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];

        args = args.splice(1);
        switch(cmd) {
            // !ping
            case 'ping':
                bot.sendMessage({
                    to: channelID,
                    message: 'Pong!'
                });
            break;
            case 'mos':
                bot.sendMessage({
                    to: channelID,
                    message: 'All hail the master of spices!'
                  });
            break;
            case 'jakejack':
                bot.sendMessage({
                    to: channelID,
                    message: 'JakeJack is taking over'
                });
            break;
            case 'jackdontcare':
                bot.sendMessage({
                    to: channelID,
                    message: 'The spiciest of them all (please jack give me more chilies)'
                });
            break;
            case 'tartarusrage':
                bot.sendMessage({
                    to: channelID,
                    message: 'Stop being sick'
                });
            break;
            case 'cheesemango':
                bot.sendMessage({
                  to: channelID,
                  message: 'No'
                });
            break;
            case 'kasumi':
                bot.sendMessage({
                  to: channelID,
                  message: 'very cool'
                });
            break;
            case 'burp':
                bot.sendMessage({
                  to: channelID,
                  message: 'burp'
              });
            break;
            case 'dragonking':
                bot.sendMessage({
                  to: channelID,
                  message: "Can't speak to women"
                });
            break;
         }
     }
});
