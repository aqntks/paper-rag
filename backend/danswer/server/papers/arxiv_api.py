import arxiv
import warnings
from typing import List
from datetime import datetime, timedelta



class ArxivAPI:
    def __init__(self, start_date, end_date):
        self.client = arxiv.Client()
        self.start_date = start_date
        self.end_date = end_date
        self.sort_criterion = {
            'LastUpdatedDate': arxiv.SortCriterion.LastUpdatedDate,
            'SubmittedDate': arxiv.SortCriterion.SubmittedDate
        }
        self.sort_order = {
            'descending': arxiv.SortOrder.Descending,
            'ascending': arxiv.SortOrder.Ascending
        }

    
    def get(self, 
            categories: List, 
            query=None, 
            max_results=None,
            sort_by='SubmittedDate',
            sort_order='descending'
        ):
        try:
            collected_paper_infos = []
            assert sort_by in ['LastUpdatedDate', 'SubmittedDate']
            assert sort_order in ['descending', 'ascending']
            sort_by_obj = self.sort_criterion[sort_by]
            sort_order_obj = self.sort_order[sort_order]
        except AssertionError:
            warnings.warn(
                f'Unsupported sort_by and sot_order, sort_by: {sort_by}, sort_order: {sort_order}', Warning)
            return collected_paper_infos
        
        query = ' OR '.join([f'cat:{cat}' for cat in categories])        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_by_obj,
            sort_order=sort_order_obj
        )

        for r in self.client.results(search):
            # get arxiv published date or updated date
            paper_date = r.updated.date() if sort_by == 'LastUpdatedDate' else r.published.date()
            
            if paper_date < self.start_date or paper_date >= self.end_date:
                return collected_paper_infos

            collected_paper_infos.append(r)
            print(paper_date)
            print(r.categories)
            print()
        
        return collected_paper_infos

            
    

if __name__ == '__main__':
    st = '2024-02-29'
    start_date = datetime.strptime(st, '%Y-%m-%d').date()
    end_date = datetime.now().date()
    categories = ['cs.AI']#, 'cs.CL', 'cs.LG', 'cs.CV']

    arxiv_api = ArxivAPI(start_date, end_date)
    papers = arxiv_api.get(categories)
    print(len(papers))
    print(papers[0])
    print(papers[0].entry_id)
    print(papers[0].__dict__.keys())
    papers[0].download_pdf(dirpath='/Users/ljm/Desktop/s3/', filename='new.pdf')
    