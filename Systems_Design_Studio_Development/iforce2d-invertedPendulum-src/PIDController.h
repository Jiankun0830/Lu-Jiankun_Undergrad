#ifndef PIDController_H
#define PIDController_H

/*
    Simple PID controller for single float variable
    http://en.wikipedia.org/wiki/PID_controller#Pseudocode
*/

class PIDController {
protected:
    float m_gainP;
    float m_gainI;
    float m_gainD;

    float m_currentError;
    float m_previousError;
    float m_integral;
    float m_output;

public:
    PIDController() {
        m_currentError = m_previousError = m_integral = m_output = 0;
        m_gainP = m_gainP = m_gainP = 1;
    }

    void setGains(float p, float i, float d) { m_gainP = p; m_gainI = i; m_gainD = d; }

    void setError( float e ) { m_currentError = e; }

    void step(float dt) {
        m_integral = dt * (m_integral + m_currentError);
        float derivative = (1/dt) * (m_currentError - m_previousError);
        m_output = m_gainP * m_currentError + m_gainI * m_integral + m_gainD * derivative;
        m_previousError = m_currentError;
    }

    float getOutput() { return m_output; }
};

#endif
