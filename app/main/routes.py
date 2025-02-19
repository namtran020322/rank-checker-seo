from flask import render_template, redirect, url_for, flash, request, send_file, session
from flask_login import login_required, current_user
from app import db
from app.main import main
from app.main.forms import KeywordSearchForm, ExportResultsForm, IndexCheckForm
from app.main.serper_service import SerperService
from app.models import KeywordSearch, SearchResult
import openpyxl
from io import BytesIO
from datetime import datetime
import csv
from urllib.parse import urlparse
import re
import math

serper_service = SerperService()

def normalize_url(url):
    """Chuẩn hóa URL để so sánh."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    parsed = urlparse(url.lower())
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path.rstrip('/')
    return f"{domain}{path}"

@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html', title='Trang chủ')

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = KeywordSearchForm()
    if form.validate_on_submit():
        keyword_url_pairs = []
        
        # Lấy cặp từ khóa + URL chính
        keyword_url_pairs.append((form.keyword.data, form.target_url.data))
        
        # Lấy các cặp từ khóa + URL bổ sung
        for key, value in request.form.items():
            if key.startswith('keyword_') and value.strip():
                pair_id = key.split('_')[1]
                url_key = f'target_url_{pair_id}'
                if url_key in request.form and request.form[url_key].strip():
                    keyword_url_pairs.append((value, request.form[url_key]))

        search_results = []
        for keyword, url in keyword_url_pairs:
            response = serper_service.search(
                keyword=keyword,
                country=form.country.data,
                device=form.device.data
            )
            
            if response:
                search = KeywordSearch(
                    keyword=keyword,
                    target_url=url,
                    country=form.country.data,
                    device=form.device.data,
                    user=current_user
                )
                db.session.add(search)
                
                results = serper_service.parse_results(response)
                target_url_normalized = normalize_url(url)
                
                found_target = False
                for result in results:
                    result_url_normalized = normalize_url(result['link'])
                    is_target = result_url_normalized == target_url_normalized
                    
                    if is_target:
                        found_target = True
                        search.target_url_rank = result['rank']
                    
                    search_result = SearchResult(
                        search=search,
                        rank=result['rank'],
                        title=result['title'],
                        link=result['link'],
                        snippet=result['snippet'],
                        is_target=is_target
                    )
                    db.session.add(search_result)
                
                if not found_target:
                    search.target_url_rank = None
                
                search_results.append(search)
            
            db.session.commit()
        
        if search_results:
            if len(search_results) == 1:
                return redirect(url_for('main.view_results', search_id=search_results[0].id))
            else:
                return redirect(url_for('main.view_multiple_results', 
                    search_ids=','.join(str(s.id) for s in search_results)))
        else:
            flash('Có lỗi xảy ra khi tìm kiếm. Vui lòng thử lại.', 'error')
    
    return render_template('main/search.html', title='Kiểm tra thứ hạng', form=form)

@main.route('/results/<int:search_id>')
@login_required
def view_results(search_id):
    search = KeywordSearch.query.get_or_404(search_id)
    if search.user_id != current_user.id:
        flash('Bạn không có quyền xem kết quả này.', 'error')
        return redirect(url_for('main.search'))
    
    export_form = ExportResultsForm()
    return render_template(
        'main/results.html',
        title='Kết quả tìm kiếm',
        search=search,
        export_form=export_form
    )

@main.route('/results/multiple/<search_ids>')
@login_required
def view_multiple_results(search_ids):
    search_ids = [int(id) for id in search_ids.split(',')]
    searches = KeywordSearch.query.filter(
        KeywordSearch.id.in_(search_ids),
        KeywordSearch.user_id == current_user.id
    ).all()
    
    if not searches:
        flash('Không tìm thấy kết quả.', 'error')
        return redirect(url_for('main.search'))
    
    export_form = ExportResultsForm()
    return render_template(
        'main/multiple_results.html',
        title='Kết quả tìm kiếm nhiều từ khóa',
        searches=searches,
        export_form=export_form
    )

@main.route('/index-check', methods=['GET', 'POST'])
@login_required
def check_index():
    form = IndexCheckForm()
    page = request.args.get('page', 1, type=int)
    per_page = 100
    
    if form.validate_on_submit():
        urls = [url.strip() for url in form.urls.data.split('\n') if url.strip()]
        results = {}
        
        for url in urls:
            normalized_url = normalize_url(url)
            # Kiểm tra xem URL có được index không bằng cách tìm kiếm site:url
            response = serper_service.search(
                keyword=f'site:{normalized_url}',
                country='us',
                device='desktop'
            )
            
            is_indexed = False
            if response and 'organic' in response:
                for result in response['organic']:
                    if normalize_url(result['link']) == normalized_url:
                        is_indexed = True
                        break
            
            results[url] = is_indexed
        
        session['index_check_results'] = results
        return redirect(url_for('main.check_index', page=1))
    
    urls = {}
    if 'index_check_results' in session:
        all_results = session['index_check_results']
        total_urls = len(all_results)
        pages = math.ceil(total_urls / per_page)
        
        # Phân trang kết quả
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        urls = dict(list(all_results.items())[start_idx:end_idx])
    else:
        pages = 1
    
    return render_template(
        'main/index_check.html',
        title='Kiểm tra Index',
        form=form,
        urls=urls,
        page=page,
        pages=pages
    )

@main.route('/export/<int:search_id>', methods=['POST'])
@login_required
def export_results(search_id):
    search = KeywordSearch.query.get_or_404(search_id)
    if search.user_id != current_user.id:
        flash('Bạn không có quyền xuất kết quả này.', 'error')
        return redirect(url_for('main.search'))
    
    form = ExportResultsForm()
    if form.validate_on_submit():
        results = search.results.all()
        
        if form.format.data == 'xlsx':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Kết quả xếp hạng"
            
            headers = ['Từ khóa', 'URL mục tiêu', 'Thứ hạng URL', 'Quốc gia', 'Thiết bị', 
                      'Thứ hạng', 'Tiêu đề', 'URL', 'Mô tả', 'Là URL mục tiêu']
            ws.append(headers)
            
            for result in results:
                ws.append([
                    search.keyword,
                    search.target_url,
                    search.target_url_rank or 'Không tìm thấy',
                    search.country,
                    search.device,
                    result.rank,
                    result.title,
                    result.link,
                    result.snippet,
                    'Có' if result.is_target else 'Không'
                ])
            
            excel_file = BytesIO()
            wb.save(excel_file)
            excel_file.seek(0)
            
            filename = f'ket_qua_thu_hang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        elif form.format.data == 'csv':
            csv_file = BytesIO()
            writer = csv.writer(csv_file)
            
            writer.writerow(['Từ khóa', 'URL mục tiêu', 'Thứ hạng URL', 'Quốc gia', 'Thiết bị', 
                           'Thứ hạng', 'Tiêu đề', 'URL', 'Mô tả', 'Là URL mục tiêu'])
            
            for result in results:
                writer.writerow([
                    search.keyword,
                    search.target_url,
                    search.target_url_rank or 'Không tìm thấy',
                    search.country,
                    search.device,
                    result.rank,
                    result.title,
                    result.link,
                    result.snippet,
                    'Có' if result.is_target else 'Không'
                ])
            
            csv_file.seek(0)
            filename = f'ket_qua_thu_hang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            return send_file(
                csv_file,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
    
    flash('Định dạng xuất không hợp lệ.', 'error')
    return redirect(url_for('main.view_results', search_id=search_id))