from crontab import CronTab
 
class CrontabControl:
    def __init__(self):
        self.cron = CronTab()
        self.job = None
        self.all_job = None
 
    # ファイルにジョブを書き込むメソッド
    def write_job(self, command, schedule, file_name):
        self.job = self.cron.new(command=command)
        self.job.setall(schedule)
        self.cron.write(file_name)
 
    # ファイル中のジョブを全て読み込むメソッド
    def read_jobs(self, file_name):
        self.all_job = CronTab(tabfile=file_name)
 
    # ジョブを監視するメソッド
    def monitor_start(self, file):
        # スケジュールを読み込む
        self.read_jobs(file)
        for result in self.all_job.run_scheduler():
            # スケジュールになるとこの中の処理が実行される
            print("予定していたスケジュールを実行しました")


def main():
    command = 'python3 ./slackbot.py'
    schedule = '*/5 * * * *'        #execute every 5 min
    file = 'output.tab'
 
    # インスタンス作成
    c = CrontabControl()
    # ファイルに書き込む
    c.write_job(command, schedule, file)
    # タスクスケジュールの監視を開始
    c.monitor_start(file)
 
if __name__ == "__main__":
    main()
