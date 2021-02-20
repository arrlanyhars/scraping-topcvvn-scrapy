import scrapy

class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = {
        'https://www.topcv.vn/tim-viec-lam-cong-nghe-cao-c10009/'
    }

    def parse_item(self, response):
        item = {}
        company_name = response.css('div #company-name h1::text').get()
        if company_name: #premium
            #top_1
            item["jobtitle"] = ''.join(response.css('div.col-sm-10 ::text').getall()).strip()
            item["company_name"] = response.css('div #company-name h1::text').get()
            item["location"] = response.css('div.premium-box-body p span::text')[-1].get()
            item["deadline"] = response.css('div.premium-box-body p span::text').get().strip()
            item["image"] = response.css('div#company-logo ::attr(src)').get()
            #description
            item["job_description"] = ''.join(response.css('div.job-data').extract())
            item["skills"] = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[5]/span/a/text()').getall()
            #top_2
            item["salary"] = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[2]/p[1]/span[2]/text()').get()
            item["job_type"] = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[2]/p[2]/span[2]/text()').get().strip()
            item["applicant"] = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[1]/p[2]/span[2]/text()').get()
            item["job_level"] = ''.join(response.css('div.col-sm-10 ::text').getall()).strip()
            item["exp"] = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[1]/p[3]/span[2]/text()').get()
            item["gender"] = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[2]/p[3]/span[2]/text()').get()
            item["city"] = response.css('div.premium-box-body p span::text')[-1].get()
        else: #non-premium
            #top
            jobtitle=response.css('span.text-dark-blue::text').get()
            item["jobtitle"] = jobtitle.replace('Tuyển',"")
            company_name = response.css('div.company-title a::text').get()
            item["company_name"] = company_name
            item["location"] = response.css('div.text-dark-gray::text').get().strip()
            deadline = response.css('div.text-dark-gray.job-deadline::text')[-1].get().strip()
            item["deadline"] = str(deadline).replace('Hạn nộp hồ sơ: ',"")
            item["image"] = response.css('img.company-logo ::attr(src)').get()
            #description
            job_description = response.css('div#col-job-left.col-md-8.col-sm-12').getall()
            job_description = str(job_description).replace('<div class="col-md-8 col-sm-12" id="col-job-left">', "")
            head, sep, tail = job_description.partition('<h2>Cách thức ứng tuyển')
            item["job_description"] = head
            item["skills"] = response.css('div span a.btn.btn-sm.btn-default.text-dark-gray::text').getall()
            #information, right
            item["salary"] = response.xpath("//*[contains(text(), 'Mức lương:')]/following-sibling::span/a/text()").get()
            item["job_type"] = response.xpath("//*[contains(text(), 'Hình thức làm việc:')]/following-sibling::span/text()").get()
            item["applicant"] = response.xpath("//*[contains(text(), 'Số lượng cần tuyển:')]/following-sibling::span/text()").get()
            item["job_level"] = response.xpath("//*[contains(text(), 'Chức vụ:')]/following-sibling::span/text()").get()
            item["exp"] = response.xpath("//*[contains(text(), 'Yêu cầu kinh nghiệm:')]/following-sibling::span/text()").get()
            item["gender"] = response.xpath("//*[contains(text(), 'Yêu cầu giới tính:')]/following-sibling::span/text()").get()
            item["city"] = response.xpath("//*[contains(text(), 'Địa điểm làm việc:')]/following-sibling::span/a/text()").getall()
        return item

    def parse(self, response):
        for post in response.css('div.col-sm-8'):
            title_url = {
                "url" : post.css('.job-title a::attr(href)').get()
            }
            link = title_url.get("url")
            if link is not None:
                yield scrapy.Request(url=link, callback=self.parse_item)

        next_page = response.css('.pagination a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)