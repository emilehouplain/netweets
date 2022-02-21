from django.db import models
from datetime import datetime


class compteTwitter(models.Model):
    
    id_compteTwitter = models.IntegerField(null=True) #Différent de la primary key
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=42, null=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(null=True)
    profile_image_url = models.fields.URLField(null=True)
    profile_url = models.fields.URLField(null=True)
    nb_followers = models.IntegerField(null=True)
    nb_friends = models.IntegerField(null=True)
    nb_tweets = models.IntegerField(null=True)
    nb_listed = models.IntegerField(null=True)
    
    last_scrap = models.DateField(null=True)#date de la dernière MAJ --> a comparer à la date du jour pour savoir si on rescrap ?
    
    class Meta: # Permet de trier ?
        verbose_name = "Compte Twitter"
        ordering = ['created_at']
    
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard dans l'administration
        """
        return self.name #affiche la liste par "name" dans l'administration
        

class tweet(models.Model):
    
    id_tweet = models.IntegerField(null=True) #Différent de la primary key

    text = models.CharField(max_length=3000)
    
    nb_reply = models.IntegerField(null=True)
    nb_rt = models.IntegerField(null=True)
    nb_like = models.IntegerField(null=True)
    nb_quote = models.IntegerField(null=True)
    
    created_at = models.DateTimeField(null=True, verbose_name="Date de création du tweet")
    
    lang = models.CharField(max_length=3000,null=True)
    
    compteTwitter = models.ForeignKey(compteTwitter, null=True, on_delete=models.CASCADE)#CASCADE = si supression du Comtep Twitter : supression de tous les Tweets associés
    
    class Meta:
        verbose_name = "Tweets"
        ordering = ['created_at']

    def __str__(self):
        return self.text
      
class jeu(models.Model):
    #double foreignKey : bonne solution
    
    compteTwitter1 = models.ForeignKey(compteTwitter, null=True, on_delete=models.CASCADE, related_name="cT1")
    compteTwitter2 = models.ForeignKey(compteTwitter, null=True, on_delete=models.CASCADE, related_name="cT2")

    win = models.ForeignKey(compteTwitter, null=True, on_delete=models.CASCADE, related_name="cT3")

    tweet = models.ForeignKey(tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True,null=True, verbose_name="Date de création du jeu")
    
    class Meta:
        verbose_name = "Jeux"
        #ordering = ['created_at']
        
    def __str__(self):
        return self.created_at
        

