"""
Gaming Workforce Observatory - Sentiment Analyzer Enterprise
Analyse avancée des sentiments des feedbacks employés gaming
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import re
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    logger.warning("Could not download NLTK data")

class GamingSentimentAnalyzer:
    """Analyseur de sentiment enterprise pour feedbacks gaming"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True,
            max_df=0.95,
            min_df=2
        )
        
        self.classifier = LogisticRegression(
            random_state=42,
            max_iter=1000,
            C=1.0
        )
        
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.stemmer = PorterStemmer()
        
        # Gaming-specific sentiment lexicon
        self.gaming_lexicon = {
            # Positive gaming terms
            'crunch': -0.8, 'overtime': -0.6, 'deadline': -0.4,
            'innovative': 0.8, 'creative': 0.7, 'challenging': 0.5,
            'rewarding': 0.8, 'exciting': 0.7, 'passionate': 0.8,
            'collaborative': 0.6, 'supportive': 0.7, 'flexible': 0.6,
            'learning': 0.5, 'growth': 0.6, 'opportunity': 0.5,
            
            # Negative gaming terms
            'burnout': -0.9, 'toxic': -0.8, 'stressful': -0.7,
            'overworked': -0.8, 'exhausted': -0.7, 'frustrated': -0.6,
            'micromanaged': -0.7, 'underpaid': -0.6, 'unfair': -0.7,
            'bureaucratic': -0.5, 'slow': -0.4, 'outdated': -0.5
        }
        
        self.model_trained = False
        self.sentiment_categories = ['negative', 'neutral', 'positive']
    
    def preprocess_text(self, text: str) -> str:
        """Prétraite le texte pour l'analyse de sentiment"""
        
        if pd.isna(text) or text == '':
            return ''
        
        # Conversion en lowercase
        text = str(text).lower()
        
        # Suppression des caractères spéciaux mais garde la ponctuation importante
        text = re.sub(r'[^a-zA-Z0-9\s\.\!\?]', ' ', text)
        
        # Suppression des espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @st.cache_data(ttl=3600)
    def train_sentiment_model(_self, feedback_data: pd.DataFrame, 
                             text_column: str = 'feedback_text',
                             label_column: str = 'sentiment_label') -> Dict[str, Any]:
        """Entraîne le modèle de sentiment sur les feedbacks gaming"""
        
        training_results = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'data_shape': feedback_data.shape,
            'model_performance': {},
            'feature_analysis': {},
            'training_status': 'failed'
        }
        
        try:
            if text_column not in feedback_data.columns:
                training_results['error'] = f"Text column '{text_column}' not found"
                return training_results
            
            # Nettoyage des données
            clean_data = feedback_data.dropna(subset=[text_column])
            
            if label_column in clean_data.columns:
                # Mode supervisé avec labels
                clean_data = clean_data.dropna(subset=[label_column])
                texts = clean_data[text_column].apply(_self.preprocess_text)
                labels = clean_data[label_column]
            else:
                # Mode semi-supervisé avec VADER comme baseline
                texts = clean_data[text_column].apply(_self.preprocess_text)
                labels = texts.apply(lambda x: _self._vader_to_category(_self.vader_analyzer.polarity_scores(x)['compound']))
            
            if len(texts) < 50:
                training_results['error'] = f"Insufficient training data: {len(texts)} samples"
                return training_results
            
            # Vectorisation TF-IDF
            X = _self.vectorizer.fit_transform(texts)
            y = labels
            
            # Division train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Entraînement du modèle
            _self.classifier.fit(X_train, y_train)
            
            # Évaluation
            y_pred = _self.classifier.predict(X_test)
            
            # Métriques de performance
            report = classification_report(y_test, y_pred, output_dict=True)
            cv_scores = cross_val_score(_self.classifier, X_train, y_train, cv=5, scoring='accuracy')
            
            training_results['model_performance'] = {
                'accuracy': report['accuracy'],
                'precision_macro': report['macro avg']['precision'],
                'recall_macro': report['macro avg']['recall'],
                'f1_macro': report['macro avg']['f1-score'],
                'cv_accuracy_mean': cv_scores.mean(),
                'cv_accuracy_std': cv_scores.std(),
                'class_distribution': y.value_counts().to_dict()
            }
            
            # Analyse des features importantes
            feature_names = _self.vectorizer.get_feature_names_out()
            feature_importance = _self.classifier.coef_
            
            # Top features par classe
            top_features = {}
            for i, sentiment in enumerate(_self.sentiment_categories):
                if i < len(feature_importance):
                    top_indices = np.argsort(feature_importance[i])[-20:]
                    top_features[sentiment] = [
                        (feature_names[idx], feature_importance[i][idx])
                        for idx in top_indices
                    ]
            
            training_results['feature_analysis'] = top_features
            training_results['training_status'] = 'success'
            _self.model_trained = True
            
            # Matrice de confusion
            cm = confusion_matrix(y_test, y_pred)
            training_results['confusion_matrix'] = cm.tolist()
            
            logger.info(f"Sentiment model trained successfully. Accuracy: {report['accuracy']:.3f}")
            
        except Exception as e:
            training_results['error'] = str(e)
            logger.error(f"Sentiment model training failed: {e}")
        
        return training_results
    
    def _vader_to_category(self, compound_score: float) -> str:
        """Convertit un score VADER en catégorie"""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_sentiment_batch(self, texts: List[str]) -> pd.DataFrame:
        """Analyse le sentiment d'une liste de textes"""
        
        results = []
        
        for i, text in enumerate(texts):
            if pd.isna(text) or text == '':
                results.append({
                    'text_id': i,
                    'original_text': text,
                    'ml_sentiment': 'neutral',
                    'ml_confidence': 0.33,
                    'vader_sentiment': 'neutral',
                    'vader_scores': {'compound': 0, 'pos': 0, 'neu': 1, 'neg': 0},
                    'gaming_adjusted_sentiment': 'neutral',
                    'final_sentiment': 'neutral'
                })
                continue
            
            # Prétraitement
            clean_text = self.preprocess_text(text)
            
            # Prédiction ML (si modèle entraîné)
            ml_sentiment = 'neutral'
            ml_confidence = 0.33
            
            if self.model_trained:
                try:
                    text_vector = self.vectorizer.transform([clean_text])
                    ml_proba = self.classifier.predict_proba(text_vector)[0]
                    ml_sentiment = self.classifier.predict(text_vector)[0]
                    ml_confidence = max(ml_proba)
                except:
                    pass
            
            # Analyse VADER
            vader_scores = self.vader_analyzer.polarity_scores(text)
            vader_sentiment = self._vader_to_category(vader_scores['compound'])
            
            # Ajustement gaming-specific
            gaming_adjusted_sentiment = self._apply_gaming_lexicon_adjustment(
                text, vader_scores, ml_sentiment
            )
            
            # Sentiment final (consensus)
            final_sentiment = self._determine_final_sentiment(
                ml_sentiment, vader_sentiment, gaming_adjusted_sentiment,
                ml_confidence
            )
            
            results.append({
                'text_id': i,
                'original_text': text,
                'ml_sentiment': ml_sentiment,
                'ml_confidence': ml_confidence,
                'vader_sentiment': vader_sentiment,
                'vader_scores': vader_scores,
                'gaming_adjusted_sentiment': gaming_adjusted_sentiment,
                'final_sentiment': final_sentiment
            })
        
        return pd.DataFrame(results)
    
    def _apply_gaming_lexicon_adjustment(self, text: str, vader_scores: Dict, 
                                       ml_sentiment: str) -> str:
        """Applique des ajustements basés sur le lexique gaming"""
        
        text_lower = text.lower()
        gaming_score_adjustment = 0
        
        # Recherche des termes gaming dans le texte
        for term, score in self.gaming_lexicon.items():
            if term in text_lower:
                gaming_score_adjustment += score
        
        # Ajustement du score VADER
        adjusted_compound = vader_scores['compound'] + gaming_score_adjustment * 0.3
        
        # Conversion en catégorie
        return self._vader_to_category(adjusted_compound)
    
    def _determine_final_sentiment(self, ml_sentiment: str, vader_sentiment: str,
                                 gaming_sentiment: str, ml_confidence: float) -> str:
        """Détermine le sentiment final basé sur consensus"""
        
        sentiments = [ml_sentiment, vader_sentiment, gaming_sentiment]
        
        # Si haute confiance ML, privilégier ML
        if ml_confidence > 0.8:
            return ml_sentiment
        
        # Sinon, vote majoritaire
        sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
        
        # Si égalité, privilégier gaming-adjusted
        max_count = max(sentiment_counts.values())
        candidates = [s for s, count in sentiment_counts.items() if count == max_count]
        
        if gaming_sentiment in candidates:
            return gaming_sentiment
        else:
            return candidates[0]
    
    def analyze_sentiment_trends(self, feedback_df: pd.DataFrame,
                                text_column: str = 'feedback_text',
                                date_column: str = 'date') -> Dict[str, Any]:
        """Analyse les tendances de sentiment dans le temps"""
        
        if text_column not in feedback_df.columns:
            return {'error': f"Text column '{text_column}' not found"}
        
        # Analyse de sentiment sur tous les textes
        texts = feedback_df[text_column].fillna('').tolist()
        sentiment_results = self.analyze_sentiment_batch(texts)
        
        # Ajout des résultats au DataFrame original
        analysis_df = feedback_df.copy()
        analysis_df['sentiment'] = sentiment_results['final_sentiment']
        analysis_df['sentiment_confidence'] = sentiment_results['ml_confidence']
        
        # Tendances temporelles si date disponible
        trends_analysis = {
            'overall_distribution': analysis_df['sentiment'].value_counts().to_dict(),
            'average_confidence': sentiment_results['ml_confidence'].mean(),
            'temporal_trends': {}
        }
        
        if date_column in analysis_df.columns:
            analysis_df[date_column] = pd.to_datetime(analysis_df[date_column], errors='coerce')
            analysis_df = analysis_df.dropna(subset=[date_column])
            
            # Tendances mensuelles
            analysis_df['year_month'] = analysis_df[date_column].dt.to_period('M')
            monthly_trends = analysis_df.groupby(['year_month', 'sentiment']).size().unstack(fill_value=0)
            
            trends_analysis['temporal_trends'] = {
                'monthly_counts': monthly_trends.to_dict(),
                'monthly_percentages': monthly_trends.div(monthly_trends.sum(axis=1), axis=0).to_dict()
            }
        
        # Analyse par département si disponible
        if 'department' in analysis_df.columns:
            dept_sentiment = analysis_df.groupby(['department', 'sentiment']).size().unstack(fill_value=0)
            trends_analysis['department_breakdown'] = dept_sentiment.to_dict()
        
        # Mots-clés par sentiment
        keywords_analysis = self._extract_keywords_by_sentiment(sentiment_results)
        trends_analysis['keywords_by_sentiment'] = keywords_analysis
        
        return trends_analysis
    
    def _extract_keywords_by_sentiment(self, sentiment_results: pd.DataFrame) -> Dict[str, List[str]]:
        """Extrait les mots-clés principaux par sentiment"""
        
        keywords_by_sentiment = {}
        
        for sentiment in ['positive', 'negative', 'neutral']:
            sentiment_texts = sentiment_results[
                sentiment_results['final_sentiment'] == sentiment
            ]['original_text'].tolist()
            
            if not sentiment_texts:
                keywords_by_sentiment[sentiment] = []
                continue
            
            # Combinaison de tous les textes du sentiment
            combined_text = ' '.join([str(text) for text in sentiment_texts])
            combined_text = self.preprocess_text(combined_text)
            
            # Extraction des mots-clés avec TF-IDF
            try:
                # Vectorisation temporaire pour ce sentiment
                temp_vectorizer = TfidfVectorizer(
                    max_features=20,
                    ngram_range=(1, 2),
                    stop_words='english'
                )
                
                tfidf_matrix = temp_vectorizer.fit_transform([combined_text])
                feature_names = temp_vectorizer.get_feature_names_out()
                scores = tfidf_matrix.toarray()[0]
                
                # Top mots-clés
                keyword_scores = list(zip(feature_names, scores))
                keyword_scores.sort(key=lambda x: x[1], reverse=True)
                
                keywords_by_sentiment[sentiment] = [kw[0] for kw in keyword_scores[:10]]
                
            except:
                keywords_by_sentiment[sentiment] = []
        
        return keywords_by_sentiment
    
    def generate_sentiment_insights(self, trends_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Génère des insights basés sur l'analyse de sentiment"""
        
        insights = []
        
        # Analyse distribution globale
        distribution = trends_analysis.get('overall_distribution', {})
        total_feedback = sum(distribution.values())
        
        if total_feedback > 0:
            negative_pct = distribution.get('negative', 0) / total_feedback * 100
            positive_pct = distribution.get('positive', 0) / total_feedback * 100
            
            if negative_pct > 40:
                insights.append({
                    'type': 'warning',
                    'title': 'Sentiment négatif élevé',
                    'description': f'{negative_pct:.1f}% des feedbacks sont négatifs',
                    'recommendation': 'Analyse approfondie des causes de mécontentement nécessaire'
                })
            elif positive_pct > 60:
                insights.append({
                    'type': 'positive',
                    'title': 'Sentiment globalement positif',
                    'description': f'{positive_pct:.1f}% des feedbacks sont positifs',
                    'recommendation': 'Maintenir les bonnes pratiques identifiées'
                })
        
        # Analyse confiance du modèle
        avg_confidence = trends_analysis.get('average_confidence', 0)
        if avg_confidence < 0.6:
            insights.append({
                'type': 'info',
                'title': 'Confiance modèle faible',
                'description': f'Confiance moyenne: {avg_confidence:.2f}',
                'recommendation': 'Entraîner le modèle avec plus de données labellisées'
            })
        
        # Analyse par département
        dept_breakdown = trends_analysis.get('department_breakdown', {})
        if dept_breakdown:
            for dept in dept_breakdown:
                dept_data = dept_breakdown[dept]
                dept_total = sum(dept_data.values())
                if dept_total > 0:
                    dept_negative_pct = dept_data.get('negative', 0) / dept_total * 100
                    if dept_negative_pct > 50:
                        insights.append({
                            'type': 'warning',
                            'title': f'Problème spécifique - {dept}',
                            'description': f'{dept_negative_pct:.1f}% de feedbacks négatifs en {dept}',
                            'recommendation': f'Focus sur les problèmes du département {dept}'
                        })
        
        return insights
    
    def render_sentiment_dashboard(self, trends_analysis: Dict[str, Any]):
        """Affiche le dashboard d'analyse de sentiment"""
        
        st.markdown("## 💬 Sentiment Analysis Dashboard")
        
        if 'error' in trends_analysis:
            st.error(trends_analysis['error'])
            return
        
        # Métriques principales
        distribution = trends_analysis.get('overall_distribution', {})
        total_feedback = sum(distribution.values())
        
        if total_feedback > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                positive_pct = distribution.get('positive', 0) / total_feedback * 100
                st.metric("😊 Positive", f"{positive_pct:.1f}%", 
                         delta=f"{distribution.get('positive', 0)} feedbacks")
            
            with col2:
                neutral_pct = distribution.get('neutral', 0) / total_feedback * 100
                st.metric("😐 Neutral", f"{neutral_pct:.1f}%",
                         delta=f"{distribution.get('neutral', 0)} feedbacks")
            
            with col3:
                negative_pct = distribution.get('negative', 0) / total_feedback * 100
                st.metric("😞 Negative", f"{negative_pct:.1f}%",
                         delta=f"{distribution.get('negative', 0)} feedbacks",
                         delta_color="inverse")
            
            with col4:
                avg_confidence = trends_analysis.get('average_confidence', 0)
                st.metric("🎯 Model Confidence", f"{avg_confidence:.2f}")
        
        # Graphique distribution
        if distribution:
            st.markdown("### 📊 Sentiment Distribution")
            
            colors = {'positive': '#27ae60', 'neutral': '#95a5a6', 'negative': '#e74c3c'}
            
            fig = px.pie(
                values=list(distribution.values()),
                names=list(distribution.keys()),
                title="Overall Sentiment Distribution",
                color=list(distribution.keys()),
                color_discrete_map=colors
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tendances temporelles
        temporal_trends = trends_analysis.get('temporal_trends', {})
        if temporal_trends.get('monthly_percentages'):
            st.markdown("### 📈 Sentiment Trends Over Time")
            
            monthly_data = temporal_trends['monthly_percentages']
            if monthly_data:
                # Conversion pour Plotly
                trend_df = pd.DataFrame(monthly_data).reset_index()
                trend_df['year_month'] = trend_df['year_month'].astype(str)
                
                fig = px.line(
                    trend_df.melt(id_vars=['year_month'], var_name='sentiment', value_name='percentage'),
                    x='year_month',
                    y='percentage',
                    color='sentiment',
                    title='Sentiment Evolution Over Time (%)',
                    color_discrete_map=colors
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Mots-clés par sentiment
        keywords = trends_analysis.get('keywords_by_sentiment', {})
        if keywords:
            st.markdown("### 🔍 Key Words by Sentiment")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**😊 Positive Keywords**")
                for kw in keywords.get('positive', [])[:8]:
                    st.write(f"• {kw}")
            
            with col2:
                st.markdown("**😐 Neutral Keywords**")
                for kw in keywords.get('neutral', [])[:8]:
                    st.write(f"• {kw}")
            
            with col3:
                st.markdown("**😞 Negative Keywords**")
                for kw in keywords.get('negative', [])[:8]:
                    st.write(f"• {kw}")
        
        # Insights et recommandations
        insights = self.generate_sentiment_insights(trends_analysis)
        if insights:
            st.markdown("### 💡 Insights & Recommendations")
            
            for insight in insights:
                icon = {'warning': '⚠️', 'positive': '✅', 'info': 'ℹ️'}.get(insight['type'], '📋')
                
                with st.expander(f"{icon} {insight['title']}"):
                    st.write(f"**Description:** {insight['description']}")
                    st.write(f"**Recommendation:** {insight['recommendation']}")
