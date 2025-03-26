from typing import List, Dict
import requests
from ..models.jd import JobDescription, AnalysisResult, Section, BiasAnalysis, ReadabilityAnalysis, SEOAnalysis
import os
from dotenv import load_dotenv

load_dotenv()

class JDAnalyzer:
    def __init__(self):
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}

    async def analyze_text(self, content: str) -> AnalysisResult:
        """
        Analyze the job description text for various aspects
        """
        # Prepare the prompt for analysis
        prompt = f"""
        Analyze the following job description and provide a detailed analysis:
        
        {content}
        
        Please provide:
        1. Section breakdown (Role Overview, Key Responsibilities, Qualifications, etc.)
        2. Bias analysis (gender-coded words, inclusivity)
        3. Readability analysis
        4. SEO analysis
        5. Overall score and improvement suggestions
        
        Format the response as JSON with the following structure:
        {{
            "sections": [
                {{"title": "section name", "content": "section content", "suggestions": ["suggestion1", "suggestion2"]}}
            ],
            "bias_analysis": {{
                "biased_terms": ["term1", "term2"],
                "suggestions": ["suggestion1", "suggestion2"],
                "inclusivity_score": 0.0-1.0
            }},
            "readability_analysis": {{
                "score": 0.0-1.0,
                "complexity": "simple/medium/complex",
                "suggestions": ["suggestion1", "suggestion2"]
            }},
            "seo_analysis": {{
                "keywords": ["keyword1", "keyword2"],
                "missing_keywords": ["keyword1", "keyword2"],
                "suggestions": ["suggestion1", "suggestion2"]
            }},
            "overall_score": 0.0-1.0,
            "improvement_suggestions": ["suggestion1", "suggestion2"]
        }}
        """

        try:
            response = requests.post(
                self.model_url,
                headers=self.headers,
                json={"inputs": prompt}
            )
            
            if response.status_code != 200:
                raise Exception(f"Error from Hugging Face API: {response.text}")

            # Parse the response and create AnalysisResult object
            analysis_data = response.json()[0]["generated_text"]
            # Convert the string response to a dictionary
            import json
            analysis_dict = json.loads(analysis_data)

            return AnalysisResult(
                sections=[Section(**section) for section in analysis_dict["sections"]],
                bias_analysis=BiasAnalysis(**analysis_dict["bias_analysis"]),
                readability_analysis=ReadabilityAnalysis(**analysis_dict["readability_analysis"]),
                seo_analysis=SEOAnalysis(**analysis_dict["seo_analysis"]),
                overall_score=analysis_dict["overall_score"],
                improvement_suggestions=analysis_dict["improvement_suggestions"]
            )

        except Exception as e:
            raise Exception(f"Error analyzing job description: {str(e)}")

    async def enhance_jd(self, jd: JobDescription) -> JobDescription:
        """
        Enhance the job description based on analysis
        """
        # First analyze the current JD
        analysis = await self.analyze_text(jd.content)

        # Prepare the prompt for enhancement
        prompt = f"""
        Enhance the following job description based on the analysis:
        
        Original JD:
        {jd.content}
        
        Analysis:
        {analysis.json()}
        
        Please provide an enhanced version of the job description that:
        1. Addresses all bias issues
        2. Improves readability
        3. Incorporates missing keywords
        4. Maintains the original structure while making it more engaging
        5. Follows Atlan's job posting format
        
        Return only the enhanced job description text.
        """

        try:
            response = requests.post(
                self.model_url,
                headers=self.headers,
                json={"inputs": prompt}
            )
            
            if response.status_code != 200:
                raise Exception(f"Error from Hugging Face API: {response.text}")

            enhanced_content = response.json()[0]["generated_text"]

            # Create enhanced JD with analysis results
            return JobDescription(
                content=enhanced_content,
                title=jd.title,
                department=jd.department,
                location=jd.location,
                employment_type=jd.employment_type
            )

        except Exception as e:
            raise Exception(f"Error enhancing job description: {str(e)}") 