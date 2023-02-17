from apscheduler.schedulers.blocking import BlockingScheduler
import runAll
import time

def start_job():
    print("执行了一次！！!")
    runAll.AllTest().run()

def stop_job():

    print("end:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def main():
    print("hello python")
    sched = BlockingScheduler()
    # 每隔5妙执行一次 可以加入 id 参数，以方便结束该定时器  sched.remove("id")
    sched.add_job(start_job, 'cron', day_of_week='5', hour='22',minute="30",second="0")
    # sched.add_job(start_job, CronTrigger.from_crontab('0/5 * * * *'))
    # 每隔3妙执行一次
    #sched.add_job(stop_job, 'cron', hour='*',minute="*",second="0/3")
    # sched.add_job(stop_job, CronTrigger.from_crontab('0/3 * * * *'))
    # sched.add_job(stop_job, 'cron', day_of_week='0-4', hour='1-23',minute="0-59",second="2")
    sched.start()

if __name__ == '__main__':
    main()

