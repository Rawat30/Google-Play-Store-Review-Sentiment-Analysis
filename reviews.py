from textblob import TextBlob

def sentiment_analysis(review):
  def getSubjectivity(text):
    try:
      return TextBlob(text).sentiment.subjectivity
    except:
      return None
  
  #Create a function to get the polarity
  def getPolarity(text):
    try:
      return TextBlob(text).sentiment.polarity
    except:
      return None

  def getAnalysis(score):
    if isinstance(score,(int,float)):
      if score < - 0.5:
        return 'Very Negative'
      elif score >= -0.5 and score < 0:
        return "Negative"
      elif score == 0:
        return 'Neutral'
      elif score > 0 and score <=0.5:
        return 'Positive'
      else:
        return 'Very Positive'
  
  #Create two new columns ‘Subjectivity’ & ‘Polarity’
  try:
    review['subjectivity'] =   getSubjectivity(review['content'])
    review ['polarity'] = getPolarity(review['content'])
    review ['analysis'] = getAnalysis(review['polarity'])
  except Exception as e:
    print(e)
  return review