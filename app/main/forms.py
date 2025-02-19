from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, URL, Length
from urllib.parse import urlparse

def validate_url(form, field):
    url = field.data.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValidationError('URL không hợp lệ')
    except:
        raise ValidationError('URL không hợp lệ')

class KeywordSearchForm(FlaskForm):
    keyword = StringField('Từ khóa', validators=[
        DataRequired(message='Vui lòng nhập từ khóa cần kiểm tra')
    ])
    
    target_url = StringField('URL cần kiểm tra', validators=[
        DataRequired(message='Vui lòng nhập URL cần kiểm tra thứ hạng'),
        validate_url
    ])
    
    country = SelectField('Quốc gia', choices=[
        ('vn', 'Việt Nam'),
        ('us', 'Hoa Kỳ'),
        ('uk', 'Anh'),
        ('sg', 'Singapore'),
        ('my', 'Malaysia'),
        ('jp', 'Nhật Bản'),
        ('kr', 'Hàn Quốc'),
        ('au', 'Úc'),
        ('ca', 'Canada'),
        ('in', 'Ấn Độ')
    ], validators=[DataRequired(message='Vui lòng chọn quốc gia')])
    
    device = SelectField('Thiết bị', choices=[
        ('desktop', 'Máy tính'),
        ('mobile', 'Di động')
    ], validators=[DataRequired(message='Vui lòng chọn loại thiết bị')])
    
    submit = SubmitField('Kiểm tra thứ hạng')

class ExportResultsForm(FlaskForm):
    format = SelectField('Định dạng xuất', choices=[
        ('xlsx', 'Excel (.xlsx)'),
        ('csv', 'CSV')
    ], validators=[DataRequired(message='Vui lòng chọn định dạng file')])
    
    submit = SubmitField('Xuất kết quả')

class IndexCheckForm(FlaskForm):
    urls = TextAreaField('Danh sách URL (mỗi URL một dòng)', validators=[
        DataRequired(message='Vui lòng nhập ít nhất một URL để kiểm tra'),
        Length(max=10000, message='Văn bản quá dài')
    ])
    
    submit = SubmitField('Kiểm tra Index')

    def validate_urls(self, field):
        urls = [url.strip() for url in field.data.split('\n') if url.strip()]
        if len(urls) > 100:
            raise ValidationError('Số lượng URL không được vượt quá 100')
        
        for url in urls:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            try:
                result = urlparse(url)
                if not all([result.scheme, result.netloc]):
                    raise ValidationError(f'URL không hợp lệ: {url}')
            except:
                raise ValidationError(f'URL không hợp lệ: {url}')