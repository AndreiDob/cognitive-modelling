def bayesFunction(p_h, p_d_given_h, p_d_given_not_h):
    '''
    input: P(H),P(D|H)andP(D|!H)
    output: P(H| D)
    '''
    p_d = p_d_given_h * p_h + p_d_given_not_h * (1 - p_h)
    p_h_given_d = p_d_given_h * p_h / p_d
    return p_h_given_d


def bayesFunctionMultipleHypotheses(prior_probabilities, likelyhood_of_data_given_hyp):
    '''
    input: P(H),P(D|H)andP(D|!H)
    output: P(H| D)
    '''
    p_d = 0
    for p_h, p_d_given_h in zip(prior_probabilities, likelyhood_of_data_given_hyp):
        p_d += p_d_given_h * p_h
    posterior_probs = []
    for p_h, p_d_given_h in zip(prior_probabilities, likelyhood_of_data_given_hyp):
        p_h_given_d = p_d_given_h * p_h / p_d
        posterior_probs.append(p_h_given_d)
    return posterior_probs


def bayesFactor(posteriors, priors):
    # BF 1 vs not1:
    posterior_odds = posteriors[0] / (1 - posteriors[0])
    prior_odds = priors[0] / (1 - priors[0])
    bayes_factor = posterior_odds / prior_odds
    print("BF 1 vs not 1:", bayes_factor)

    if len(posteriors) == 1:
        return

    # BF 1 vs 2:
    posterior_odds = posteriors[0] / posteriors[1]
    prior_odds = priors[0] / (priors[1])
    bayes_factor = posterior_odds / prior_odds
    print("BF 1 vs 2:", bayes_factor)

    # BF 1 vs 3:
    posterior_odds = posteriors[0] / posteriors[2]
    prior_odds = priors[0] / priors[2]
    bayes_factor = posterior_odds / prior_odds
    print("BF 1 vs 3:", bayes_factor)


if __name__ == '__main__':
    # print(bayesFunctionMultipleHypotheses([0.1], [0.9], 0.3))
    # print(bayesFunctionMultipleHypotheses([0.9], [0.9], 0.3))
    # print(bayesFunctionMultipleHypotheses([0.9], [0.3], 0.9))
    # print(bayesFunctionMultipleHypotheses([0.001], [0.99], 0.02))
    # print(bayesFunctionMultipleHypotheses([0.3], [0.5], 0.5))

    # print(bayesFunctionMultipleHypotheses([0.4, 0.3, 0.3], [0.99, 0.9, 0.2]))
    # print(bayesFunctionMultipleHypotheses([0.3, 0.3, 0.4], [0.9, 0.2, 0.2]))

    # bayesFactor((0.9, 0.05, 0.05), (0.2, 0.6, 0.2))
    # bayesFactor((0.85, 0.05, 0.1), (0.2, 0.6, 0.2))

    # print(bayesFunction(0.5, 0.531, 0.52))
    # posteriors = []
    # posteriors.append(bayesFunction(0.5, 0.531, 0.52))
    # bayesFactor(posteriors, [0.5])
    #
    # # p_h, p_d_given_h, p_d_given_not_h):
    # p_h = bayesFunction(0.001, 0.531, 0.52)
    # p_not_h = bayesFunction(1-0.001, 0.52, 0.531)
    # posterior_odds = p_h / p_not_h
    # print("posterior_odds", posterior_odds)

    # exercise D
    posterior1_prior2 = bayesFunction(0.5, 0.531, 0.52)
    posterior2_prior3 = bayesFunction(posterior1_prior2, 0.471, 0.52)
    posterior3_prior4 = bayesFunction(posterior2_prior3, 0.491, 0.65)
    posterior4_prior5 = bayesFunction(posterior3_prior4, 0.505, 0.7)

    print(f"Posterior after experiment 2: {posterior2_prior3}")
    print(f"Posterior after experiment 3: {posterior3_prior4}")
    print(f"Posterior after experiment 4: {posterior4_prior5}")

    '''
    input: P(H),P(D|H)andP(D|!H)
    output: P(H| D)
    '''
