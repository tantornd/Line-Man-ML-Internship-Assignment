import http from 'k6/http';
import {check} from 'k6';
import {SharedArray} from 'k6/data';

const r = new SharedArray('requests', function () {
    return JSON.parse(open('../data/request.json'));
});

export const options = {
    scenarios: {
        testt: {
            executor: "constant-arrival-rate",
            rate: 30, timeUnit: "1s",
            duration: "2m",
            preAllocatedVUs: 50,
        },
    },
    thresholds: {
        http_req_duration: ['p(90) < 100'],
    },
};

export default function () {
    const x = r[Math.floor(Math.random() * r.length)];
    let maxDis = x.max_dis;
    if (maxDis === null || maxDis === undefined) {
        maxDis = 5000;}
    let sortDis = x.sort_dis;
    if (sortDis === null || sortDis === undefined) {
        sortDis = 0;}
    let url = `http://localhost:80/recommend/${x.user_id}?latitude=${x.latitude}&longitude=${x.longitude}&size=${x.size}&max_dis=${maxDis}&sort_dis=${sortDis}`;
    let response = http.get(url);
    check(response, {
        'all queries are correct': (res) => res.status === 200,
        'less than 100ms': (res) => res.timings.duration < 100,
    });
}
