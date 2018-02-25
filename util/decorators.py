from util.timer import feedback_msg


def feedback_timer(input_function):
    def wrapper(bot, update, user_data, job_queue):
        input_function(bot, update, user_data, job_queue)
        for item in job_queue.queue.queue:
            item[1].schedule_removal()
        job_queue.run_once(feedback_msg, 10, context=update)
        # TODO : Need to fix the time which was kept as 5 for testing purposes
    return wrapper
