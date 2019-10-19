This program takes in a text file 'SMScollection.txt' which containes 5574 messages. Each line of the file is represents one SMS/text
message. The first item on every line is a label - 'ham' or 'spam' - indicating whether that line's SMS is considered spam or not. The 
rest of the line contains the text of the SMS/message. For example:
    spam:  Congrats! 1 year special cinema pass for 2 is yours. call 09061209465 now! Call ...
    ham:	Sorry, I'll call later in meeting.
    
My program analyzing the text messages file and prints out the following:
      1.the number of ham and number of spam messages
      2.the total number of words found in ham messages and in spam messages
      3.the number of unique words found in ham messages and in spam messages
      4.information, for both ham and for spam, about the twelve (at least) most frequently occurring words that are at least minWordLengthToConsider characters long. This information must include both the count of the number of occurrences and the relative frequency of a word's occurrence as a percentage (how many times that word appears out of the total number of words in the relevant message set. For example, if "you" appeared 80 times in ham, out of 1250 total ham word occurrences, the frequency would be 6.4%).
      5.the average length (in words, not characters) of ham messages and of spam messages
