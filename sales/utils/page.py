from django.utils.safestring import mark_safe


class MyPage:
    def __init__(self, cur_page, per_page_num, page_tag_num, customers_total_count, base_url, url_par):
        try:
            cur_page = int(cur_page)  # 防止随意输入非数字字符
        except Exception:
            cur_page = 1

        self.per_page_num = per_page_num
        self.page_tag_num = page_tag_num
        self.base_url = base_url
        self.url_par = url_par
        # merchant 商, remainder 余数
        merchant, remainder = divmod(customers_total_count, self.per_page_num)
        self.page_tag_total = merchant + 1 if remainder else merchant  # 分页显示总数

        if cur_page <= 0:
            cur_page = 1
        elif cur_page >= self.page_tag_total:
            cur_page = self.page_tag_total
        if self.page_tag_total == 0:
            cur_page = 1
        self.cur_page = cur_page
        half_page_tag = page_tag_num // 2  # 12345
        if self.cur_page - half_page_tag <= 0:
            start_page_num = 1
            end_page_num = page_tag_num + 1
        elif self.cur_page + half_page_tag >= self.page_tag_total:
            start_page_num = self.page_tag_total - page_tag_num + 1
            end_page_num = self.page_tag_total + 1
        else:
            start_page_num = self.cur_page - half_page_tag
            end_page_num = self.cur_page + half_page_tag + 1
        self.start_page_num = start_page_num
        self.end_page_num = end_page_num
        if self.page_tag_total < page_tag_num:
            self.start_page_num = 1
            self.end_page_num = self.page_tag_total + 1

    @property
    def start_html_num(self):
        return (self.cur_page - 1) * self.per_page_num

    @property
    def end_html_num(self):
        return self.cur_page * self.per_page_num

    @property
    def b_url(self):
        return self.url_par.urlencode()

    def page_html(self):
        page_num_range = range(self.start_page_num, self.end_page_num)
        page_html = ''
        page_html += f'<nav aria-label="Page navigation" class="pull-right"><ul class="pagination">'
        self.url_par['page'] = 1
        page_html += f'<li><a href="{self.base_url}?{self.url_par.urlencode()}" aria-label="Previous">' \
                     f'<span aria-hidden="true">首页</span></a></li>'
        if self.cur_page <= 1:
            pre_page = '<li class="disabled"><a href="javascript:void(0)" ' \
                       'aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            self.url_par['page'] = self.cur_page - 1
            pre_page = f'<li><a href="{self.base_url}?{self.url_par.urlencode()}" aria-label="Previous">' \
                       f'<span aria-hidden="true">&laquo;</span></a></li>'
        page_html += pre_page
        for i in page_num_range:
            self.url_par['page'] = i
            if i == self.cur_page:
                page_html += f'<li class="active"><a href="{self.base_url}?{self.url_par.urlencode()}">{i}</a></li>'
            else:
                page_html += f'<li><a href="{self.base_url}?{self.url_par.urlencode()}">{i}</a></li>'

        if self.cur_page >= self.page_tag_total:
            page_html += f'<li class="disabled"><a href="javascript:void(0)" ' \
                         f'aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            self.url_par['page'] = self.cur_page + 1
            page_html += f'<li><a href="{self.base_url}?{self.url_par.urlencode()}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        self.url_par['page'] = self.page_tag_total
        page_html += f'<li><a href="{self.base_url}?{self.url_par.urlencode()}" aria-label="Previous">' \
                     f'<span aria-hidden="true">尾页</span></a></li>'
        page_html += f'</ul></nav>'

        return mark_safe(page_html)
